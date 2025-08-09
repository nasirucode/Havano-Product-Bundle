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
			if item.product_bundle:
				# Handle product bundle items
				bundle_items = get_product_bundle_items(item.product_bundle)
				for bundle_item in bundle_items:
					# Create stock entry for bundle items
					create_bundle_stock_entry(doc, item, bundle_item)


def handle_bundle_stock_entry_cancel(doc, method):
	"""Handle cancellation of product bundle items in Stock Entry"""
	if doc.purpose == "Material Transfer":
		for item in doc.items:
			if item.product_bundle:
				# Cancel stock entry for bundle items
				cancel_bundle_stock_entry(doc, item)


def handle_bundle_material_request(doc, method):
	"""Handle product bundle items in Material Request"""
	for item in doc.items:
		if item.product_bundle:
			# Handle product bundle items
			bundle_items = get_product_bundle_items(item.product_bundle)
			for bundle_item in bundle_items:
				# Create material request for bundle items
				create_bundle_material_request(doc, item, bundle_item)


def handle_bundle_material_request_cancel(doc, method):
	"""Handle cancellation of product bundle items in Material Request"""
	for item in doc.items:
		if item.product_bundle:
			# Cancel material request for bundle items
			cancel_bundle_material_request(doc, item)


def handle_bundle_purchase_receipt(doc, method):
	"""Handle product bundle items in Purchase Receipt"""
	for item in doc.items:
		if item.product_bundle:
			# Handle product bundle items
			bundle_items = get_product_bundle_items(item.product_bundle)
			for bundle_item in bundle_items:
				# Create purchase receipt for bundle items
				create_bundle_purchase_receipt(doc, item, bundle_item)


def handle_bundle_purchase_receipt_cancel(doc, method):
	"""Handle cancellation of product bundle items in Purchase Receipt"""
	for item in doc.items:
		if item.product_bundle:
			# Cancel purchase receipt for bundle items
			cancel_bundle_purchase_receipt(doc, item)


def handle_bundle_purchase_invoice(doc, method):
	"""Handle product bundle items in Purchase Invoice"""
	for item in doc.items:
		if item.product_bundle:
			# Handle product bundle items
			bundle_items = get_product_bundle_items(item.product_bundle)
			for bundle_item in bundle_items:
				# Create purchase invoice for bundle items
				create_bundle_purchase_invoice(doc, item, bundle_item)


def handle_bundle_purchase_invoice_cancel(doc, method):
	"""Handle cancellation of product bundle items in Purchase Invoice"""
	for item in doc.items:
		if item.product_bundle:
			# Cancel purchase invoice for bundle items
			cancel_bundle_purchase_invoice(doc, item)


def create_bundle_stock_entry(parent_doc, parent_item, bundle_item):
	"""Create stock entry for bundle items"""
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
		"serial_no": parent_item.serial_no,
		"batch_no": parent_item.batch_no
	})
	
	stock_entry.insert()
	stock_entry.submit()
	
	return stock_entry.name


def cancel_bundle_stock_entry(parent_doc, parent_item):
	"""Cancel stock entry for bundle items"""
	# Find and cancel related stock entries
	stock_entries = frappe.get_all("Stock Entry", 
		filters={
			"reference_doctype": parent_doc.doctype,
			"reference_name": parent_doc.name,
			"docstatus": 1
		})
	
	for se in stock_entries:
		try:
			se_doc = frappe.get_doc("Stock Entry", se.name)
			se_doc.cancel()
		except Exception as e:
			frappe.log_error(f"Error cancelling stock entry {se.name}: {str(e)}")


def create_bundle_material_request(parent_doc, parent_item, bundle_item):
	"""Create material request for bundle items"""
	material_request = frappe.new_doc("Material Request")
	material_request.material_request_type = "Purchase"
	material_request.company = parent_doc.company
	material_request.posting_date = parent_doc.posting_date
	material_request.set_warehouse = parent_item.warehouse
	
	# Calculate quantities
	bundle_qty = flt(parent_item.qty) * flt(bundle_item.qty)
	
	material_request.append("items", {
		"item_code": bundle_item.item_code,
		"qty": bundle_qty,
		"uom": bundle_item.uom,
		"warehouse": parent_item.warehouse,
		"description": bundle_item.description
	})
	
	material_request.insert()
	material_request.submit()
	
	return material_request.name


def cancel_bundle_material_request(parent_doc, parent_item):
	"""Cancel material request for bundle items"""
	# Find and cancel related material requests
	material_requests = frappe.get_all("Material Request", 
		filters={
			"reference_doctype": parent_doc.doctype,
			"reference_name": parent_doc.name,
			"docstatus": 1
		})
	
	for mr in material_requests:
		try:
			mr_doc = frappe.get_doc("Material Request", mr.name)
			mr_doc.cancel()
		except Exception as e:
			frappe.log_error(f"Error cancelling material request {mr.name}: {str(e)}")


def create_bundle_purchase_receipt(parent_doc, parent_item, bundle_item):
	"""Create purchase receipt for bundle items"""
	purchase_receipt = frappe.new_doc("Purchase Receipt")
	purchase_receipt.company = parent_doc.company
	purchase_receipt.posting_date = parent_doc.posting_date
	purchase_receipt.posting_time = parent_doc.posting_time
	purchase_receipt.set_posting_time = parent_doc.set_posting_time
	
	# Calculate quantities
	bundle_qty = flt(parent_item.qty) * flt(bundle_item.qty)
	
	purchase_receipt.append("items", {
		"item_code": bundle_item.item_code,
		"qty": bundle_qty,
		"uom": bundle_item.uom,
		"warehouse": parent_item.warehouse,
		"description": bundle_item.description,
		"rate": parent_item.rate or 0,
		"amount": flt(bundle_qty) * flt(parent_item.rate or 0),
		"serial_no": parent_item.serial_no,
		"batch_no": parent_item.batch_no
	})
	
	purchase_receipt.insert()
	purchase_receipt.submit()
	
	return purchase_receipt.name


def cancel_bundle_purchase_receipt(parent_doc, parent_item):
	"""Cancel purchase receipt for bundle items"""
	# Find and cancel related purchase receipts
	purchase_receipts = frappe.get_all("Purchase Receipt", 
		filters={
			"reference_doctype": parent_doc.doctype,
			"reference_name": parent_doc.name,
			"docstatus": 1
		})
	
	for pr in purchase_receipts:
		try:
			pr_doc = frappe.get_doc("Purchase Receipt", pr.name)
			pr_doc.cancel()
		except Exception as e:
			frappe.log_error(f"Error cancelling purchase receipt {pr.name}: {str(e)}")


def create_bundle_purchase_invoice(parent_doc, parent_item, bundle_item):
	"""Create purchase invoice for bundle items"""
	purchase_invoice = frappe.new_doc("Purchase Invoice")
	purchase_invoice.company = parent_doc.company
	purchase_invoice.posting_date = parent_doc.posting_date
	purchase_invoice.posting_time = parent_doc.posting_time
	purchase_invoice.set_posting_time = parent_doc.set_posting_time
	
	# Calculate quantities
	bundle_qty = flt(parent_item.qty) * flt(bundle_item.qty)
	
	purchase_invoice.append("items", {
		"item_code": bundle_item.item_code,
		"qty": bundle_qty,
		"uom": bundle_item.uom,
		"warehouse": parent_item.warehouse,
		"description": bundle_item.description,
		"rate": parent_item.rate or 0,
		"amount": flt(bundle_qty) * flt(parent_item.rate or 0),
		"serial_no": parent_item.serial_no,
		"batch_no": parent_item.batch_no
	})
	
	purchase_invoice.insert()
	purchase_invoice.submit()
	
	return purchase_invoice.name


def cancel_bundle_purchase_invoice(parent_doc, parent_item):
	"""Cancel purchase invoice for bundle items"""
	# Find and cancel related purchase invoices
	purchase_invoices = frappe.get_all("Purchase Invoice", 
		filters={
			"reference_doctype": parent_doc.doctype,
			"reference_name": parent_doc.name,
			"docstatus": 1
		})
	
	for pi in purchase_invoices:
		try:
			pi_doc = frappe.get_doc("Purchase Invoice", pi.name)
			pi_doc.cancel()
		except Exception as e:
			frappe.log_error(f"Error cancelling purchase invoice {pi.name}: {str(e)}")


@frappe.whitelist()
def get_bundle_stock_balance(product_bundle, warehouse=None):
	"""Get stock balance for a product bundle"""
	if not product_bundle:
		return 0
	
	bundle_items = get_product_bundle_items(product_bundle)
	total_balance = 0
	
	for bundle_item in bundle_items:
		balance = frappe.db.get_value("Bin", {
			"item_code": bundle_item.item_code,
			"warehouse": warehouse
		}, "actual_qty") or 0
		
		# Calculate bundle balance based on bundle item quantity
		bundle_balance = flt(balance) / flt(bundle_item.qty) if bundle_item.qty else 0
		total_balance = min(total_balance, bundle_balance) if total_balance > 0 else bundle_balance
	
	return total_balance
