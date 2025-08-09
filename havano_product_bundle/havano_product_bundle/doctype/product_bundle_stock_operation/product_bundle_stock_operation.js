// Copyright (c) 2025, Havano Product Bundle and contributors
// For license information, please see license.txt

frappe.ui.form.on('Product Bundle Stock Operation', {
	refresh: function(frm) {
		// Add button to load bundle items
		if (frm.doc.product_bundle && !frm.doc.items.length) {
			frm.add_custom_button(__('Load Bundle Items'), function() {
				frm.events.load_bundle_items(frm);
			}).addClass('btn-primary');
		}
		
		// Add button to create ERPNext document
		if (frm.doc.status === 'Draft' && frm.doc.items.length > 0) {
			frm.add_custom_button(__('Submit'), function() {
				frm.submit();
			}).addClass('btn-primary');
		}
		
		// Add button to cancel
		if (frm.doc.status === 'Submitted') {
			frm.add_custom_button(__('Cancel'), function() {
				frm.cancel();
			}).addClass('btn-danger');
		}
	},
	
	product_bundle: function(frm) {
		// Clear items when product bundle changes
		frm.clear_table('items');
		frm.refresh_field('items');
	},
	
	operation_type: function(frm) {
		// Set warehouse fields based on operation type
		if (frm.doc.operation_type === 'Material Transfer') {
			frm.set_df_property('source_warehouse', 'reqd', 1);
			frm.set_df_property('target_warehouse', 'reqd', 1);
		} else if (frm.doc.operation_type === 'Material Request') {
			frm.set_df_property('source_warehouse', 'reqd', 0);
			frm.set_df_property('target_warehouse', 'reqd', 1);
		} else if (frm.doc.operation_type in ['Purchase Receipt', 'Purchase Invoice']) {
			frm.set_df_property('source_warehouse', 'reqd', 0);
			frm.set_df_property('target_warehouse', 'reqd', 1);
		}
	},
	
	load_bundle_items: function(frm) {
		if (!frm.doc.product_bundle) {
			frappe.msgprint(__('Please select a Product Bundle first'));
			return;
		}
		
		frappe.call({
			method: 'havano_product_bundle.havano_product_bundle.doctype.product_bundle_stock_operation.product_bundle_stock_operation.load_bundle_items',
			args: {
				product_bundle: frm.doc.product_bundle
			},
			callback: function(r) {
				if (r.message) {
					frm.clear_table('items');
					
					r.message.forEach(function(bundle_item) {
						let item = frm.add_child('items');
						item.item_code = bundle_item.item_code;
						item.qty = bundle_item.qty;
						item.uom = bundle_item.uom;
						item.description = bundle_item.description;
						item.warehouse = frm.doc.target_warehouse || frm.doc.source_warehouse;
					});
					
					frm.refresh_field('items');
					frm.calculate_totals();
				}
			}
		});
	},
	
	calculate_totals: function(frm) {
		let total_qty = 0;
		let total_amount = 0;
		
		frm.doc.items.forEach(function(item) {
			total_qty += flt(item.qty);
			total_amount += flt(item.amount);
		});
		
		frm.set_value('total_qty', total_qty);
		frm.set_value('total_amount', total_amount);
		frm.set_value('base_total_amount', total_amount);
	}
});

// Child table events
frappe.ui.form.on('Product Bundle Stock Operation Item', {
	qty: function(frm, cdt, cdn) {
		calculate_amount(frm, cdt, cdn);
		frm.events.calculate_totals(frm);
	},
	
	rate: function(frm, cdt, cdn) {
		calculate_amount(frm, cdt, cdn);
		frm.events.calculate_totals(frm);
	},
	
	item_code: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		if (row.item_code) {
			// Fetch item details
			frappe.call({
				method: 'frappe.client.get_value',
				args: {
					doctype: 'Item',
					filters: { name: row.item_code },
					fieldname: ['item_name', 'description', 'stock_uom', 'default_warehouse']
				},
				callback: function(r) {
					if (r.message) {
						row.item_name = r.message.item_name;
						row.uom = r.message.stock_uom;
						row.description = r.message.description;
						if (!row.warehouse) {
							row.warehouse = r.message.default_warehouse;
						}
						frm.refresh_field('items');
					}
				}
			});
		}
	}
});

function calculate_amount(frm, cdt, cdn) {
	let row = locals[cdt][cdn];
	if (row.qty && row.rate) {
		row.amount = flt(row.qty) * flt(row.rate);
		frm.refresh_field('amount', cdn);
	}
}


