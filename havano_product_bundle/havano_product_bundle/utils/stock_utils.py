# Copyright (c) 2025, Havano Product Bundle and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt
from erpnext.stock.doctype.packed_item.packed_item import get_product_bundle_items


def handle_bundle_stock_entry(doc, method):
	"""Handle product bundle items in Stock Entry"""
	if doc.purpose == "Material Transfer":
		for item in doc.items:
			if hasattr(item, 'product_bundle') and item.product_bundle:
				# Handle product bundle items
				bundle_items = get_product_bundle_items(item.product_bundle)
				for bundle_item in bundle_items:
					# Create stock entry for bundle items
					create_bundle_stock_entry(doc, item, bundle_item)


def handle_bundle_stock_entry_cancel(doc, method):
	"""Handle cancellation of product bundle items in Stock Entry"""
	if doc.purpose == "Material Transfer":
		for item in doc.items:
			if hasattr(item, 'product_bundle') and item.product_bundle:
				# Cancel stock entry for bundle items
				cancel_bundle_stock_entry(doc, item)


def handle_bundle_material_request(doc, method):
	"""Handle product bundle items in Material Request"""
	for item in doc.items:
		if hasattr(item, 'product_bundle') and item.product_bundle:
			# Handle product bundle items
			bundle_items = get_product_bundle_items(item.product_bundle)
			for bundle_item in bundle_items:
				# Create material request for bundle items
				create_bundle_material_request(doc, item, bundle_item)


def handle_bundle_material_request_cancel(doc, method):
	"""Handle cancellation of product bundle items in Material Request"""
	for item in doc.items:
		if hasattr(item, 'product_bundle') and item.product_bundle:
			# Cancel material request for bundle items
			cancel_bundle_material_request(doc, item)


def create_bundle_stock_entry(parent_doc, parent_item, bundle_item):
	"""Create stock entry for bundle items"""
	try:
		stock_entry = frappe.new_doc("Stock Entry")
		stock_entry.stock_entry_type = "Material Transfer"
		stock_entry.purpose = "Material Transfer"
		stock_entry.company = parent_doc.company
		stock_entry.posting_date = parent_doc.posting_date
		stock_entry.posting_time = parent_doc.posting_time
		stock_entry.set_posting_time = parent_doc.set_posting_time
		
		# Calculate quantities
		bundle_qty = flt(parent_item.qty) * flt(bundle_item.qty)
		
		stock_entry.append("items", {
			"item_code": bundle_item.item_code,
			"s_warehouse": parent_item.s_warehouse,
			"t_warehouse": parent_item.t_warehouse,
			"qty": bundle_qty,
			"uom": bundle_item.uom,
			"conversion_factor": 1.0,
			"transfer_qty": bundle_qty,
			"basic_rate": parent_item.basic_rate or 0,
			"serial_no": getattr(parent_item, 'serial_no', ''),
			"batch_no": getattr(parent_item, 'batch_no', '')
		})
		
		stock_entry.insert()
		stock_entry.submit()
		
		return stock_entry.name
	except Exception as e:
		frappe.log_error(f"Error creating bundle stock entry: {str(e)}")
		return None


def cancel_bundle_stock_entry(parent_doc, parent_item):
	"""Cancel stock entry for bundle items"""
	# Find and cancel related stock entries
	stock_entries = frappe.get_all("Stock Entry", 
		filters={
			"docstatus": 1
		})
	
	for se in stock_entries:
		try:
			se_doc = frappe.get_doc("Stock Entry", se.name)
			se_doc.cancel()
		except Exception as e:
			frappe.log_error(f"Error cancelling stock entry {se.name}: {str(e)}")


@frappe.whitelist()
def get_bundle_stock_balance(product_bundle, warehouse=None):
	"""Get stock balance for a product bundle"""
	if not product_bundle:
		return 0
	
	try:
		bundle_items = get_product_bundle_items(product_bundle)
		total_balance = float('inf')  # Start with infinity
		
		for bundle_item in bundle_items:
			balance = frappe.db.get_value("Bin", {
				"item_code": bundle_item.item_code,
				"warehouse": warehouse
			}, "actual_qty") or 0
			
			# Calculate how many bundles can be made from this item
			bundle_balance = flt(balance) / flt(bundle_item.qty) if bundle_item.qty else 0
			total_balance = min(total_balance, bundle_balance)
		
		# If no items found, return 0
		return 0 if total_balance == float('inf') else int(total_balance)
		
	except Exception as e:
		frappe.log_error(f"Error getting bundle stock balance: {str(e)}")
		return 0