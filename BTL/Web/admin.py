from Web import app, db, utils
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, AdminIndexView
from Web.models import Category, Medicine, Rule, Receipt, ReceiptDetail, UserRole, DanhSachKham, \
    PhieuKham, ToaThuoc, ChiTietToaThuoc, User, Guest, Doctor, Nurse, Cashier, Manager, City, District, Ward
from flask_login import current_user, logout_user
from flask import redirect, request, url_for, render_template
from datetime import datetime


def check_manager():
    manager = utils.get_manager_by_id(current_user.id)
    if manager:
        return True
    else:
        return False


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated \
               and current_user.user_role.__eq__(UserRole.ADMIN) \
               and check_manager()


class CategoryView(AuthenticatedView):
    can_view_details = True
    can_export = True
    details_modal = True
    edit_modal = True
    create_modal = True
    column_display_pk = True
    column_searchable_list = ['name']


class PhieuKhamView(AuthenticatedView):
    can_view_details = True
    can_export = True
    details_modal = True
    edit_modal = True
    create_modal = True
    column_display_pk = True


class ChiTietToaThuocView(AuthenticatedView):
    can_view_details = True
    can_export = True
    details_modal = True
    edit_modal = True
    create_modal = True
    column_display_pk = True


class MedicineView(AuthenticatedView):
    can_view_details = True
    can_export = True
    details_modal = True
    edit_modal = True
    create_modal = True
    column_display_pk = True
    column_searchable_list = ['name', 'description']
    column_filters = ['name', 'price']
    column_exclude_list = ['active']
    column_sortable_list = ['id', 'name', 'price']
    column_editable_list = ['name', 'unit']


class RuleView(AuthenticatedView):
    can_view_details = True
    can_export = True
    details_modal = True
    edit_modal = True
    create_modal = True
    column_display_pk = True


class UserView(AuthenticatedView):
    can_view_details = True
    can_export = True
    details_modal = True
    edit_modal = True
    create_modal = True
    column_display_pk = True
    column_searchable_list = ['name', 'username']
    column_exclude_list = ['email', 'avatar']
    column_editable_list = ['name', 'username', 'user_role']


class GuestView(AuthenticatedView):
    can_view_details = True
    can_export = True
    details_modal = True
    edit_modal = True
    create_modal = True
    column_display_pk = True
    column_searchable_list = ['name', 'username']
    column_exclude_list = ['email', 'avatar']
    column_editable_list = ['name', 'username', 'user_role']


class DoctorView(AuthenticatedView):
    can_view_details = True
    can_export = True
    details_modal = True
    edit_modal = True
    create_modal = True
    column_display_pk = True
    column_searchable_list = ['name', 'username']
    column_exclude_list = ['email', 'avatar']
    column_editable_list = ['name', 'username', 'user_role']


class Cities(AuthenticatedView):
    can_view_details = True
    can_export = True
    details_modal = True
    edit_modal = True
    create_modal = True
    column_display_pk = True


class Countries(AuthenticatedView):
    can_view_details = True
    can_export = True
    details_modal = True
    edit_modal = True
    create_modal = True
    column_display_pk = True


class CashierView(AuthenticatedView):
    can_view_details = True
    can_export = True
    details_modal = True
    edit_modal = True
    create_modal = True
    column_display_pk = True
    column_searchable_list = ['name', 'username']
    column_exclude_list = ['email', 'avatar']
    column_editable_list = ['name', 'username', 'user_role']


class ManagerView(AuthenticatedView):
    can_view_details = True
    can_export = True
    details_modal = True
    edit_modal = True
    create_modal = True
    column_display_pk = True
    column_searchable_list = ['name', 'username']
    column_exclude_list = ['email', 'avatar']
    column_editable_list = ['name', 'username', 'user_role']


class NurseView(AuthenticatedView):
    can_view_details = True
    can_export = True
    details_modal = True
    edit_modal = True
    create_modal = True
    column_display_pk = True
    column_searchable_list = ['name', 'username']
    column_exclude_list = ['email', 'avatar']
    column_editable_list = ['name', 'username', 'user_role']


class ToaThuocView(AuthenticatedView):
    can_view_details = True
    can_export = True
    details_modal = True
    edit_modal = True
    create_modal = True
    column_display_pk = True


class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and check_manager()


class LogoutView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        user = User.query.get(current_user.id)
        user.active = False
        db.session.add(user)
        db.session.commit()
        logout_user()
        return redirect('/admin')


class StatsView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        kw = request.args.get('kw')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        year = request.args.get('year', datetime.now().year)
        month = request.args.get('month')
        day = request.args.get('day')
        return self.render('admin/stats.html',
                           month_stats=utils.medicine_month_stats(year=year,
                                                                  month=month,
                                                                  day=day,
                                                                  from_date=from_date,
                                                                  to_date=to_date),
                           medicine_stats=utils.medicine_stats(year=year,
                                                               month=month,
                                                               day=day,
                                                               kw=kw,
                                                               from_date=from_date,
                                                               to_date=to_date))


class Calculate(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        return self.render('admin/calculator.html')


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html',
                           stats=utils.category_stats())


class Account(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        city = utils.load_city()
        district = utils.load_district()
        ward = utils.load_ward()
        return self.render('admin/account_info.html',
                           city=city,
                           district=district,
                           ward=ward)


class ShowReceipt(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        receipt_id = request.args.get('receipt_id')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        year = request.args.get('year')
        month = request.args.get('month')
        day = request.args.get('day', datetime.now().day)
        return self.render('admin/ReceiptDetail.html',
                           receipt=utils.get_receipt_detail_by_id(receipt_id=receipt_id,
                                                                  year=year,
                                                                  month=month,
                                                                  day=day,
                                                                  from_date=from_date,
                                                                  to_date=to_date))


admin = Admin(app=app,
              name='Administration',
              template_mode='bootstrap4',
              index_view=MyAdminIndexView())

admin.add_view(CategoryView(Category, db.session))
admin.add_view(MedicineView(Medicine, db.session))
admin.add_view(UserView(User, db.session))
admin.add_view(NurseView(Nurse, db.session))
admin.add_view(GuestView(Guest, db.session))
admin.add_view(CashierView(Cashier, db.session))
admin.add_view(DoctorView(Doctor, db.session))
admin.add_view(ManagerView(Manager, db.session))
admin.add_view(Cities(City, db.session))
admin.add_view(ModelView(District, db.session))
admin.add_view(ModelView(Ward, db.session))
# admin.add_view(Countries(Country, db.session))
# admin.add_view(RuleView(Rule, db.session))
admin.add_view(StatsView(name='Stats'))
# admin.add_view(Calculate(name='Calculate'))
admin.add_view(Account(name='Account'))
admin.add_view(ShowReceipt(name='ReceiptDetail'))
# admin.add_view(PhieuKhamView(PhieuKham, db.session))
# admin.add_view(ToaThuocView(ToaThuoc, db.session))
# admin.add_view(ChiTietToaThuocView(ChiTietToaThuoc, db.session))
# admin.add_view(AuthenticatedView(Receipt, db.session))
# admin.add_view(AuthenticatedView(ReceiptDetail, db.session))
admin.add_view(LogoutView(name='Logout'))
