# Copyright (c) 2025, Havano Product Bundle and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, now_datetime
from erpnext.stock.doctype.packed_item.packed_item import get_product_bundle_items


class ProductBundleStockOperation(Document):
	def validate(self):
		self.validate_operation_type()
		self.validate_warehouses()
		self.calculate_totals()
	
	def on_submit(self):
		self.create_erpnext_document()
	
	def on_cancel(self):
		self.cancel_erpnext_document()
	
	def validate_operation_type(self):
		"""Validate operation type and set required fields"""
		if self.operation_type == "Material Transfer":
			if not self.source_warehouse:
				frappe.throw(_("Source Warehouse is required for Material Transfer"))
			if not self.target_warehouse:
				frappe.throw(_("Target Warehouse is required for Material Transfer"))
		
		elif self.operation_type == "Material Request":
			if not self.target_warehouse:
				frappe.throw(_("Target Warehouse is required for Material Request"))
		
		elif self.operation_type in ["Purchase Receipt", "Purchase Invoice"]:
			if not self.target_warehouse:
				frappe.throw(_("Target Warehouse is required for Purchase operations"))
	
	def validate_warehouses(self):
		"""Validate warehouse settings based on operation type"""
		if self.operation_type == "Material Transfer":
			if self.source_warehouse == self.target_warehouse:
				frappe.throw(_("Source and Target warehouses cannot be the same"))
	
	def calculate_totals(self):
		"""Calculate totals from items"""
		total_qty = 0
		total_amount = 0
		
		for item in self.items:
			total_qty += flt(item.qty)
			total_amount += flt(item.amount)
		
		self.total_qty = total_qty
		self.total_amount = total_amount
		self.base_total_amount = total_amount  # Assuming same currency for now
	
	def load_product_bundle_items(self):
		"""Load items from product bundle"""
		if not self.product_bundle:
			return
		
		# Clear existing items
		self.items = []
		
		# Get bundle items
		bundle_items = get_product_bundle_items(self.product_bundle)
		
		for bundle_item in bundle_items:
			self.append("items", {
				"item_code": bundle_item.item_code,
				"qty": bundle_item.qty,
				"uom": bundle_item.uom,
				"description": bundle_item.description,
				"warehouse": self.target_warehouse or self.source_warehouse
			})
	
	def create_erpnext_document(self):
		"""Create corresponding ERPNext document based on operation type"""
		if self.operation_type == "Material Transfer":
			self.create_stock_entry()
		elif self.operation_type == "Material Request":
			self.create_material_request()
		elif self.operation_type == "Purchase Receipt":
			self.create_purchase_receipt()
		elif self.operation_type == "Purchase Invoice":
			self.create_purchase_invoice()
	
	def create_stock_entry(self):
		"""Create Stock Entry for Material Transfer"""
		stock_entry = frappe.new_doc("Stock Entry")
		stock_entry.stock_entry_type = "Material Transfer"
		stock_entry.purpose = "Material Transfer"
		stock_entry.company = self.company
		stock_entry.posting_date = self.posting_date
		stock_entry.posting_time = self.posting_time
		stock_entry.set_posting_time = self.set_posting_time
		
		# Add items
		for item in self.items:
			stock_entry.append("items", {
				"item_code": item.item_code,
				"s_warehouse": self.source_warehouse,
				"t_warehouse": self.target_warehouse,
				"qty": item.qty,
				"uom": item.uom,
				"conversion_factor": item.conversion_factor,
				"transfer_qty": item.stock_qty,
				"basic_rate": item.rate,
				"serial_no": item.serial_no,
				"batch_no": item.batch_no
			})
		
		stock_entry.insert()
		stock_entry.submit()
		
		# Update reference
		self.reference_doctype = "Stock Entry"
		self.reference_name = stock_entry.name
		self.save()
	
	def create_material_request(self):
		"""Create Material Request"""
		material_request = frappe.new_doc("Material Request")
		material_request.material_request_type = "Purchase"
		material_request.company = self.company
		material_request.posting_date = self.posting_date
		material_request.set_warehouse = self.target_warehouse
		
		# Add items
		for item in self.items:
			material_request.append("items", {
				"item_code": item.item_code,
				"qty": item.qty,
				"uom": item.uom,
				"warehouse": self.target_warehouse,
				"description": item.description
			})
		
		material_request.insert()
		material_request.submit()
		
		# Update reference
		self.reference_doctype = "Material Request"
		self.reference_name = material_request.name
		self.save()
	
	def create_purchase_receipt(self):
		"""Create Purchase Receipt"""
		purchase_receipt = frappe.new_doc("Purchase Receipt")
		purchase_receipt.company = self.company
		purchase_receipt.posting_date = self.posting_date
		purchase_receipt.posting_time = self.posting_time
		purchase_receipt.set_posting_time = self.set_posting_time
		
		# Add items
		for item in self.items:
			purchase_receipt.append("items", {
				"item_code": item.item_code,
				"qty": item.qty,
				"uom": item.uom,
				"warehouse": self.target_warehouse,
				"description": item.description,
				"rate": item.rate,
				"amount": item.amount,
				"serial_no": item.serial_no,
				"batch_no": item.batch_no
			})
		
		purchase_receipt.insert()
		purchase_receipt.submit()
		
		# Update reference
		self.reference_doctype = "Purchase Receipt"
		self.reference_name = purchase_receipt.name
		self.save()
	
	def create_purchase_invoice(self):
		"""Create Purchase Invoice"""
		purchase_invoice = frappe.new_doc("Purchase Invoice")
		purchase_invoice.company = self.company
		purchase_invoice.posting_date = self.posting_date
		purchase_invoice.posting_time = self.posting_time
		purchase_invoice.set_posting_time = self.set_posting_time
		
		# Add items
		for item in self.items:
			purchase_invoice.append("items", {
				"item_code": item.item_code,
				"qty": item.qty,
				"uom": item.uom,
				"warehouse": self.target_warehouse,
				"description": item.description,
				"rate": item.rate,
				"amount": item.amount,
				"serial_no": item.serial_no,
				"batch_no": item.batch_no
			})
		
		purchase_invoice.insert()
		purchase_invoice.submit()
		
		# Update reference
		self.reference_doctype = "Purchase Invoice"
		self.reference_name = purchase_invoice.name
		self.save()
	
	def cancel_erpnext_document(self):
		"""Cancel the corresponding ERPNext document"""
		if self.reference_doctype and self.reference_name:
			try:
				doc = frappe.get_doc(self.reference_doctype, self.reference_name)
				if doc.docstatus == 1:  # Submitted
					doc.cancel()
			except Exception as e:
				frappe.log_error(f"Error cancelling {self.reference_doctype} {self.reference_name}: {str(e)}")


@frappe.whitelist()
def load_bundle_items(product_bundle):
	"""Load items from product bundle"""
	if not product_bundle:
		return []
	
	bundle_items = get_product_bundle_items(product_bundle)
	return bundle_items


