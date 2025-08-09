# Copyright (c) 2025, Havano Product Bundle and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute():
	"""Add stock support fields to Product Bundle"""
	
	# Add stock support fields to Product Bundle
	if not frappe.db.exists("Custom Field", "Product Bundle-stock_item"):
		frappe.get_doc({
			"doctype": "Custom Field",
			"dt": "Product Bundle",
			"fieldname": "stock_item",
			"label": "Is Stock Item",
			"fieldtype": "Check",
			"default": "0",
			"description": "Enable stock management for this product bundle",
			"insert_after": "disabled"
		}).insert()
	
	if not frappe.db.exists("Custom Field", "Product Bundle-maintain_stock"):
		frappe.get_doc({
			"doctype": "Custom Field",
			"dt": "Product Bundle",
			"fieldname": "maintain_stock",
			"label": "Maintain Stock",
			"fieldtype": "Check",
			"default": "0",
			"description": "Maintain stock for this product bundle",
			"insert_after": "stock_item"
		}).insert()
	
	if not frappe.db.exists("Custom Field", "Product Bundle-stock_uom"):
		frappe.get_doc({
			"doctype": "Custom Field",
			"dt": "Product Bundle",
			"fieldname": "stock_uom",
			"label": "Stock UOM",
			"fieldtype": "Link",
			"options": "UOM",
			"description": "Stock UOM for the product bundle",
			"insert_after": "maintain_stock"
		}).insert()
	
	# Add stock support fields to Product Bundle Item
	if not frappe.db.exists("Custom Field", "Product Bundle Item-stock_qty"):
		frappe.get_doc({
			"doctype": "Custom Field",
			"dt": "Product Bundle Item",
			"fieldname": "stock_qty",
			"label": "Stock Quantity",
			"fieldtype": "Float",
			"read_only": 1,
			"description": "Stock quantity for this bundle item",
			"insert_after": "qty"
		}).insert()
	
	if not frappe.db.exists("Custom Field", "Product Bundle Item-warehouse"):
		frappe.get_doc({
			"doctype": "Custom Field",
			"dt": "Product Bundle Item",
			"fieldname": "warehouse",
			"label": "Warehouse",
			"fieldtype": "Link",
			"options": "Warehouse",
			"description": "Default warehouse for this bundle item",
			"insert_after": "stock_qty"
		}).insert()
	
	frappe.db.commit()


