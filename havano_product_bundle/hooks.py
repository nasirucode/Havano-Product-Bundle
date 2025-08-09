app_name = "havano_product_bundle"
app_title = "Havano Product Bundle"
app_publisher = "nasirucode"
app_description = "Havano Product Bundle"
app_email = "akingbolahan12@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "havano_product_bundle",
# 		"logo": "/assets/havano_product_bundle/logo.png",
# 		"title": "Havano Product Bundle",
# 		"route": "/havano_product_bundle",
# 		"has_permission": "havano_product_bundle.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/havano_product_bundle/css/havano_product_bundle.css"
# app_include_js = "/assets/havano_product_bundle/js/havano_product_bundle.js"

# include js, css files in header of web template
# web_include_css = "/assets/havano_product_bundle/css/havano_product_bundle.css"
# web_include_js = "/assets/havano_product_bundle/js/havano_product_bundle.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "havano_product_bundle/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "havano_product_bundle/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "havano_product_bundle.utils.jinja_methods",
# 	"filters": "havano_product_bundle.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "havano_product_bundle.install.before_install"
# after_install = "havano_product_bundle.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "havano_product_bundle.uninstall.before_uninstall"
# after_uninstall = "havano_product_bundle.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "havano_product_bundle.utils.before_app_install"
# after_app_install = "havano_product_bundle.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "havano_product_bundle.utils.before_app_uninstall"
# after_app_uninstall = "havano_product_bundle.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "havano_product_bundle.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Product Bundle": {
		"on_update": "havano_product_bundle.havano_product_bundle.doctype.product_bundle_stock_operation.product_bundle_stock_operation.update_bundle_stock",
		"validate": "havano_product_bundle.havano_product_bundle.doctype.product_bundle_stock_operation.product_bundle_stock_operation.validate_bundle_stock"
	},
	"Stock Entry": {
		"on_submit": "havano_product_bundle.havano_product_bundle.utils.stock_utils.handle_bundle_stock_entry",
		"on_cancel": "havano_product_bundle.havano_product_bundle.utils.stock_utils.handle_bundle_stock_entry_cancel"
	},
	"Material Request": {
		"on_submit": "havano_product_bundle.havano_product_bundle.utils.stock_utils.handle_bundle_material_request",
		"on_cancel": "havano_product_bundle.havano_product_bundle.utils.stock_utils.handle_bundle_material_request_cancel"
	},
	"Purchase Receipt": {
		"on_submit": "havano_product_bundle.havano_product_bundle.utils.stock_utils.handle_bundle_purchase_receipt",
		"on_cancel": "havano_product_bundle.havano_product_bundle.utils.stock_utils.handle_bundle_purchase_receipt_cancel"
	},
	"Purchase Invoice": {
		"on_submit": "havano_product_bundle.havano_product_bundle.utils.stock_utils.handle_bundle_purchase_invoice",
		"on_cancel": "havano_product_bundle.havano_product_bundle.utils.stock_utils.handle_bundle_purchase_invoice_cancel"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"havano_product_bundle.tasks.all"
# 	],
# 	"daily": [
# 		"havano_product_bundle.tasks.daily"
# 	],
# 	"hourly": [
# 		"havano_product_bundle.tasks.hourly"
# 	],
# 	"weekly": [
# 		"havano_product_bundle.tasks.weekly"
# 	],
# 	"monthly": [
# 		"havano_product_bundle.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "havano_product_bundle.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "havano_product_bundle.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "havano_product_bundle.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["havano_product_bundle.utils.before_request"]
# after_request = ["havano_product_bundle.utils.after_request"]

# Job Events
# ----------
# before_job = ["havano_product_bundle.utils.before_job"]
# after_job = ["havano_product_bundle.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"havano_product_bundle.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

