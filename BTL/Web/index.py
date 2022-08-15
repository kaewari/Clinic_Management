import hashlib

import MySQLdb
import requests
import datetime
from flask import render_template, url_for, session, jsonify
from Web.admin import *
from Web import login
import utils
from Web.models import User
from flask_login import login_user, login_required, current_user
from datetime import timedelta, date, datetime
from twilio.rest import Client
import cloudinary.uploader
from sqlalchemy import func, extract


@app.route("/")
def home():
    return render_template('index.html')


def check_doctor():
    doctor = utils.get_doctor_by_id(current_user.id)
    if doctor:
        return True
    else:
        return False


def check_user():
    user = utils.get_user_by_id(current_user.id)
    if user:
        return True
    else:
        return False


def check_nurse():
    nurse = utils.get_nurse_by_id(current_user.id)
    if nurse:
        return True
    else:
        return False


def check_cashier():
    cashier = utils.get_cashier_by_id(current_user.id)
    if cashier:
        return True
    else:
        return False


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=15)


@app.route('/user-login', methods=['get', 'post'])
def user_login():
    error_msg = ""
    if request.method.__eq__('POST'):
        try:
            username = request.form['username']
            password = request.form['password']

            user = utils.check_login(username=username, password=password, user_role=UserRole.USER)
            if user:
                login_user(user=user)
                user = User.query.get(current_user.id)
                user.active = True
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('home'))
            else:
                error_msg = "Chuong trinh dang co loi! Vui long quay lai sau!"

        except Exception as ex:
            error_msg = str(ex)

    return render_template('login.html', error_msg=error_msg)


@app.route('/user-logout')
def logout():
    user = User.query.get(current_user.id)
    if user:
        user.active = False
        db.session.add(user)
        db.session.commit()
    logout_user()
    return redirect(url_for('home'))


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.route('/admin/admin-login', methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = utils.check_login(username=username,
                             password=password,
                             user_role=UserRole.ADMIN)
    if user and UserRole.ADMIN:
        login_user(user=user)
        user = User.query.get(current_user.id)
        user.active = True
        db.session.add(user)
        db.session.commit()
    return redirect('/admin')


@app.route("/admin/account", methods=['get', 'post'])
@login_required
def admin_account():
    data = request.form.copy()
    if request.method.__eq__('POST'):

        file = request.files['avatar']
        if file:
            res = cloudinary.uploader.upload(file)
            data['avatar'] = res['secure_url']
    utils.change_new_info(**data)

    return redirect(url_for('admin_account'))


@app.route("/admin/account/password", methods=['get', 'post'])
@login_required
def change_admin_password_account():
    error_msg = ""
    if request.method.__eq__('POST'):
        old_password = request.form['password']
        password = hashlib.md5(old_password.strip().encode('utf-8')).hexdigest()
        new_password = request.form['new_password']
        confirm = request.form['confirm']
        if password.__eq__(current_user.password) and new_password.__eq__(confirm):
            data = request.form.copy()
            del data['confirm']
            del data['password']
            if utils.change_new_password(new_password=new_password):
                return redirect('/admin')
    return render_template('change_admin_password.html', error_msg=error_msg)


@app.route("/password", methods=['get', 'post'])
@login_required
def change_user_password():
    error_msg = ""
    if request.method.__eq__('POST'):
        try:
            old_password = request.form.get('password')
            password = hashlib.md5(old_password.strip().encode('utf-8')).hexdigest()
            new_password = request.form.get('new_password')
            confirm = request.form.get('confirm')
            if password.__eq__(current_user.password) and new_password.__eq__(confirm):
                data = request.form.copy()
                del data['confirm']
                del data['password']
                if utils.change_new_password(**data):
                    logout_user()
                else:
                    error_msg = "Chuong trinh dang co loi! Vui long quay lai sau!"
        except Exception as ex:
            error_msg = str(ex)
    return render_template('change_user_password.html', error_msg=error_msg)


@app.route("/register", methods=['get', 'post'])
def register():
    error_msg = ""
    city = utils.load_city()
    district = utils.load_district()
    ward = utils.load_ward()
    if request.method.__eq__('POST'):
        try:
            password = request.form['password']
            confirm = request.form['confirm']
            if password.__eq__(confirm):
                data = request.form.copy()

                del data['confirm']

                file = request.files['avatar']
                if file:
                    res = cloudinary.uploader.upload(file)
                    data['avatar'] = res['secure_url']

                if utils.create_user(**data):
                    return redirect(url_for('user_login'))
                else:
                    error_msg = "Chuong trinh dang co loi! Vui long quay lai sau!"
            else:
                error_msg = "Mat khau KHONG khop!"
        except Exception as ex:
            error_msg = str(ex)

    return render_template('register.html', city=city, district=district, ward=ward, error_msg=error_msg)


@app.route("/account", methods=['get', 'post'])
@login_required
def user_info():
    city = utils.load_city()
    ward = utils.load_ward()
    district = utils.load_district()
    data = request.form.copy()
    if request.method.__eq__('POST'):
        file = request.files['avatar']
        if file:
            res = cloudinary.uploader.upload(file)
            data['avatar'] = res['secure_url']
    utils.change_new_info(**data)
    return render_template('account_info_user.html', city=city, district=district, ward=ward)


@app.route("/account/password", methods=['get', 'post'])
@login_required
def change_admin_password():
    error_msg = ""
    if request.method.__eq__('POST'):
        try:
            old_password = request.form['password']
            password = hashlib.md5(old_password.strip().encode('utf-8')).hexdigest()
            new_password = request.form['new_password']
            confirm = request.form['confirm']
            if password.__eq__(current_user.password) and new_password.__eq__(confirm):
                data = request.form.copy()
                del data['confirm']
                del data['password']
                if utils.change_new_password(**data):
                    logout_user()
                    redirect(url_for('admin'))
                else:
                    error_msg = "Chuong trinh dang co loi! Vui long quay lai sau!"
        except Exception as ex:
            error_msg = str(ex)
    return render_template('change_admin_password.html', error_msg=error_msg)


@app.route("/appointment", methods=['get', 'post'])
def appointment():
    error_msg = ""
    if request.method.__eq__('POST'):
        data = request.form.copy()
        ID_card = request.form['ID_card']
        phone_number = request.form['phone_number']
        created_date = request.form['created_date']
        current_date = datetime.now()
        if check_user():
            if len(str(ID_card)) != 12:
                error_msg = "CCCD Không tồn tại"
            else:
                if len(phone_number) > 11 or len(phone_number) < 10:
                    error_msg = "SĐT không tồn tại"
                else:
                    if created_date < str(current_date):
                        error_msg = "Lịch đặt khám không phù hợp"
                    else:
                        if utils.create_appointment(**data):
                            return redirect(url_for('home'))
                        else:
                            error_msg = "Chuong trinh dang co loi! Vui long quay lai sau!"
        else:
            error_msg = "Không được phép đăng ký"
    return render_template('appointment.html', error_msg=error_msg)


@app.errorhandler(404)
def Web_Not_Found(e):
    return render_template('404.html')


@app.route('/employee/add-receipt/cart', methods=['get', 'post'])
@login_required
def create_cart():
    err_msg = "Không được phép truy cập"
    if check_cashier():
        return render_template('employee/cart.html',
                               stats=utils.count_cart(session.get('cart')))
    else:
        return render_template('employee/index.html', err_msg=err_msg)


@app.context_processor
def common_response():
    return {
        'cart_stats': utils.count_cart(session.get('cart')),
        'prescription_stats': utils.count(session.get('form'))
    }


@app.route('/api/add-cart', methods=['post'])
def add_to_cart():
    data = request.json
    id = str(data.get('id'))
    name = data.get('name')
    price = data.get('price')

    cart = session.get('cart')
    if not cart:
        cart = {}

    if id in cart:
        cart[id]['quantity'] = cart[id]['quantity'] + 1
    else:
        cart[id] = {
            'id': id,
            'name': name,
            'price': price,
            'quantity': 1
        }

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route('/api/delete-cart/<medicine_id>', methods=['delete'])
def delete_cart(medicine_id):
    cart = session.get('cart')
    if cart and medicine_id in cart:
        del cart[medicine_id]
        session['cart'] = cart
    return jsonify(utils.count_cart(cart))


@app.route('/employee/pay', methods=['post'])
@login_required
def pay():
    err_msg = ""
    try:
        toathuoc_id = request.form.get('toathuoc_id')
        guest_id = request.form.get('guest_id')
        medical_expense = request.form.get('medical_expense')
        if guest_id == "" or toathuoc_id == "" or medical_expense == "":
            err_msg = "CHƯA NHẬP ĐỦ THÔNG TIN YÊU CẦU"
        else:
            utils.add_receipt(session.get('cart'), medical_expense=medical_expense, toathuoc_id=toathuoc_id, guest_id=guest_id)
            del session['cart']
    except Exception as ex:
        err_msg = str(ex)
    return render_template('employee/cart.html', err_msg=err_msg)


@app.route('/api/add-form', methods=['post'])
def add_to_form():
    data = request.json
    id = str(data.get('id'))
    name = data.get('name')

    form = session.get('form')
    if not form:
        form = {}

    if id in form:
        form[id]['quantity'] = form[id]['quantity'] + 1
    else:
        form[id] = {
            'id': id,
            'name': name,
            'quantity': 1
        }

    session['form'] = form

    return jsonify(utils.count(form))


@app.route('/api/delete-form/<medicine_id>', methods=['delete'])
def delete_form(medicine_id):
    form = session.get('form')
    if form and medicine_id in form:
        del form[medicine_id]
        session['form'] = form
    return jsonify(utils.count(form))


@app.route('/employee/add-form/prescription')
@login_required
def create_prescription():
    err_msg = "Không được phép truy cập"
    if check_doctor():
        cate_id = request.args.get('category_id')
        kw = request.args.get('kw')
        id = request.args.get('id')
        return render_template('employee/prescription.html',
                               medicine=utils.load_medicine(cate_id=cate_id, kw=kw, id=id),
                               categories=utils.load_categories())
    else:
        return render_template('employee/index.html', err_msg=err_msg)


@app.route('/employee/add-form/create-form', methods=['get', 'post'])
@login_required
def create_medical_form():
    err_msg = "Không được phép truy cập"
    if check_doctor():
        return render_template('employee/medical_form.html',
                               prescription_stats=utils.count(session.get('form')))
    else:
        return render_template('employee/index.html', err_msg=err_msg)


@app.route('/employee/create-form-done', methods=['post'])
@login_required
def create_form_done():
    err_msg = ""
    try:
        symptom = request.form.get('symptom')
        diagnose_disease = request.form.get('diagnose_disease')
        how_to_use = request.form.get('how_to_use')
        guest_id = request.form.get('guest_id')
        if symptom and diagnose_disease:
            utils.add_medical_form(session.get('form'), guest_id=guest_id, symptom=symptom,
                                   diagnose_disease=diagnose_disease, how_to_use=how_to_use)
            del session['form']
        else:
            if guest_id == "" or how_to_use == "" or symptom == "" or diagnose_disease == "":
                err_msg = "CHƯA NHẬP ĐỦ THÔNG TIN YÊU CẦU"
    except Exception as ex:
        err_msg = str(ex)
    return render_template('employee/medical_form.html', err_msg=err_msg)


@app.route('/employee/list-form', methods=['post', 'get'])
@login_required
def List_form():
    err_msg = "Không được phép truy cập"
    if check_nurse():
        day = request.args.get('day', datetime.now().day)
        guest_id = request.form.get('guest_id')
        data = request.form.copy()
        if guest_id == "":
            err_msg = "Chưa nhập đủ thông tin"
            return render_template('employee/list.html',
                                   list=utils.count_list(day=day),
                                   count=utils.count_patient(),
                                   err_msg=err_msg)
        else:
            if request.method.__eq__('POST'):
                utils.save_danhsachkham_info(**data)
            return render_template('employee/list.html',
                                   count=utils.count_patient(),
                                   list=utils.count_list())
    else:
        return render_template('employee/index.html',
                               err_msg=err_msg)


@app.route('/employee/create_list', methods=['get', 'post'])
@login_required
def create_list():
    err_msg = "Không được phép truy cập"
    if check_nurse():
        nurse_id = request.form.get('nurse_id')
        if nurse_id == "":
            err_msg = "Chưa nhập đủ thông tin"
            return render_template('employee/create_list.html',
                                   list=utils.count_list(),
                                   err_msg=err_msg)
        else:
            if request.method.__eq__('POST'):
                utils.create_list()
                return redirect(url_for('create_list'))
            return render_template('employee/create_list.html',
                                   list=utils.count_list())
    else:
        return render_template('employee/index.html',
                               err_msg=err_msg)


@app.route('/employee/create_list/<int:danhsachkham_id>', methods=['get', 'post'])
@login_required
def delete_list(danhsachkham_id):
    err_msg = "Không được phép truy cập"
    if check_nurse():
        utils.delete_list(danhsachkham_id)
        return redirect(url_for('delete_list'))
    else:
        return render_template('employee/index.html',
                               err_msg=err_msg)


@app.route('/employee/add-form/form', methods=['get', 'post'])
@login_required
def form():
    if check_doctor():
        guest_id = request.args.get('guest_id')
        year = request.args.get('year')
        month = request.args.get('month')
        day = request.args.get('day', datetime.now().day)
        if guest_id == "" or (day == "" and month == "" and year == ""):
            err_msg = "Chưa nhập đủ thông tin. Bạn cần nhập mã bệnh nhân và (ngày hoặc tháng hoặc năm)"
            return render_template('employee/form.html', err_msg=err_msg)
        else:
            return render_template('employee/form.html',
                                   form=utils.find_guest_in_form(guest_id=guest_id, day=day, month=month, year=year),
                                   toathuoc=utils.find_toathuoc_in_form(guest_id=guest_id, day=day, month=month, year=year))
    else:
        err_msg = "Không được phép truy cập"
        return render_template('employee/index.html', err_msg=err_msg)


@app.route('/employee')
def employee():
    cate_id = request.args.get('category_id')
    kw = request.args.get('kw')
    return render_template('employee/index.html',
                           medicine=utils.load_medicine(cate_id=cate_id, kw=kw),
                           categories=utils.load_categories())


@app.route('/employee/medicine/<int:medicine_id>')
def medicine_detail(medicine_id):
    med = utils.get_medicine_by_id(medicine_id=medicine_id)
    return render_template('employee/medicine_detail.html',
                           med=med)


@app.route('/employee/login', methods=['get', 'post'])
def employee_login():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = utils.check_login(username=username,
                                 password=password,
                                 user_role=UserRole.EMPLOYEE)
        if user and UserRole.EMPLOYEE:
            login_user(user=user)
            user = User.query.get(current_user.id)
            user.active = True
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('employee'))
        else:
            err_msg = 'Username hoac password khong chinh xac!!!'
    return render_template('employee/login.html', err_msg=err_msg)


@app.route('/employee/add-receipt/receipt')
@login_required
def receipt():
    err_msg = "không được phép truy cập"
    if check_cashier():
        guest_id = request.args.get('guest_id')
        year = request.args.get('year')
        month = request.args.get('month')
        day = request.args.get('day', datetime.now().day)
        if guest_id == "" or (day == "" and month == "" and year == ""):
            err_msg = "Chưa nhập đủ thông tin. Bạn cần nhập mã bệnh nhân và (ngày hoặc tháng hoặc năm)"
            return render_template('employee/create_receipt.html', err_msg=err_msg)
        else:
            return render_template('employee/create_receipt.html',
                                   receipt=utils.get_receipt_in_receipt_info(guest_id=guest_id, day=day, month=month, year=year))
    else:
        return render_template('employee/index.html', err_msg=err_msg)


@app.route('/employee/add-form')
@login_required
def Add_form():
    err_msg = "Không được phép truy cập"
    if check_doctor():
        cate_id = request.args.get('category_id')
        kw = request.args.get('kw')
        return render_template('employee/prescription.html',
                               medicine=utils.load_medicine(cate_id=cate_id, kw=kw),
                               categories=utils.load_categories())
    else:
        return render_template('employee/index.html', err_msg=err_msg)


@app.route('/employee/add-receipt')
@login_required
def Add_receipt():
    err_msg = "không được phép truy cập"
    if check_cashier():
        cate_id = request.args.get('category_id')
        id = request.args.get('id')
        return render_template('employee/pay.html',
                               receipt=utils.load_receipt(),
                               medicine=utils.load_medicine(cate_id=cate_id, id=id),
                               categories=utils.load_categories(),
                               receipt_detail=utils.load_receipt_detail())
    else:
        return render_template('employee/index.html', err_msg=err_msg)


@app.route('/employee/add-receipt/medical-form-detail')
def medical_form_detail():
    err_msg = "không được phép truy cập"
    if check_cashier():
        kw = request.args.get('kw')
        return render_template('employee/Medical_form_detail.html',
                               details=utils.load_form(kw=kw))
    else:
        return render_template('employee/index.html', err_msg=err_msg)


@app.route('/employee/list-form/send-sms', methods=['get', 'post'])
@login_required
def Send_SMS():
    err_msg = "Không được phép truy cập"
    if check_nurse():
        msg, notify = "", "Không nhập số 0 ở đầu SĐT"
        if request.method.__eq__('POST'):
            phone_number = request.form['phone_number']
            content = request.form.get('content')
            from twilio.rest import Client
            if len(str(phone_number)) >= 11:
                msg = "Không thành công"
            else:
                account_sid = 'AC1a6ce6e2a699cab0a48f6276a324f498'
                auth_token = '1e4176afda37fbf90913964dbf764de9'
                client = Client(account_sid, auth_token)

                message = client.messages.create(
                    messaging_service_sid='MG7bd0604d2846a90668deab79fcf9ed39',
                    from_='+19522609468',
                    body="XIN CHÀO " + str(content) + ". BẠN ĐÃ ĐƯỢC THÊM VÀO DANH SÁCH CỦA PHÒNG KHÁM",
                    to='+84' + phone_number
                )
                if message.sid:
                    msg = message.sid
        return render_template('employee/send_sms.html', msg=msg, notify=notify)
    else:
        return render_template('employee/index.html', err_msg=err_msg)


@app.route('/employee/add-receipt/medical-form-detail/detail/<int:toathuoc_id>')
def toathuoc_detail(toathuoc_id):
    err_msg = "không được phép truy cập"
    if check_cashier():
        toathuoc = utils.get_chitiet_toathuoc_by_id(toathuoc_id=toathuoc_id)
        return render_template('employee/toathuoc_detail.html', toathuoc=toathuoc)
    else:
        return render_template('employee/index.html', err_msg=err_msg)


@app.route('/employee/add-form/guest-detail/detail/<int:guest_id>')
def guest_detail(guest_id):
    err_msg = "Không được phép truy cập"
    if check_doctor():
        guest = utils.get_guest_by_id(guest_id=guest_id)

        return render_template('employee/guest_detail.html', guest=guest)
    else:
        return render_template('employee/index.html', err_msg=err_msg)


@app.route('/employee/account/', methods=['get', 'post'])
@login_required
def employee_account():
    data = request.form.copy()
    if request.method.__eq__('POST'):
        file = request.files['avatar']
        if file:
            res = cloudinary.uploader.upload(file)
            data['avatar'] = res['secure_url']
    utils.change_new_info(**data)
    return render_template('employee/account_info.html')


@app.route("/employee/account/password", methods=['get', 'post'])
@login_required
def change_employee_password_account():
    error_msg = ""
    if request.method.__eq__('POST'):
        old_password = request.form['password']
        password = hashlib.md5(old_password.strip().encode('utf-8')).hexdigest()
        new_password = request.form['new_password']
        confirm = request.form['confirm']
        if password.__eq__(current_user.password) and new_password.__eq__(confirm):
            data = request.form.copy()
            del data['confirm']
            del data['password']
            if utils.change_new_password(**data):
                logout_user()
                return redirect(url_for('employee_login'))
    return render_template('change_admin_password.html', error_msg=error_msg)


@app.route('/employee/list-form/appointment')
def show_appointment():
    err_msg = "Không được phép truy cập"
    if check_nurse():
        kw = request.args.get('kw')
        year = request.args.get('year')
        month = request.args.get('month')
        day = request.args.get('day', datetime.now().day)
        return render_template('employee/show_appointment.html',
                               appointment=utils.load_appointment(kw=kw, day=day, month=month, year=year))
    else:
        return render_template('employee/index.html', err_msg=err_msg)


@app.route('/employee/add-form/guest-list')
def guest_list():
    kw = request.args.get('kw')
    return render_template('employee/show_guest.html',
                           guest_list=utils.load_guest(kw=kw))


@app.route('/employee/show-list')
def show_list():
    day = request.args.get('day', datetime.now().day)
    return render_template('employee/show_list.html',
                           show_list=utils.show_list(day=day))


@app.route('/employee/guest')
def guest():
    kw = request.args.get('kw')
    return render_template('employee/show_guest_nurse.html',
                           guest=utils.load_guest(kw=kw))


@app.route('/employee/guest/guest-detail/<int:guest_id>')
def detail(guest_id):
    err_msg = "Không được phép truy cập"
    if check_nurse():
        guest = utils.get_guest_by_id(guest_id=guest_id)
        appointment = utils.get_appointment_by_id(guest_id=guest_id)
        return render_template('employee/guest_detail_nurse.html', guest=guest, appointment=appointment)
    else:
        return render_template('employee/index.html', err_msg=err_msg)


@app.route('/intro')
def intro():
    return render_template('introduction.html')


@app.route('/show-employee')
def show_employee():
    return render_template('show_employee.html',
                           employee=utils.load_employee())


@app.route('/building')
def building():
    return render_template('building.html')


@app.route('/open-door')
def open_door():
    return render_template('open_door.html')


@app.route('/news')
def news():
    return render_template('news.html')


@app.route('/ask')
def ask():
    return render_template('ask.html')


@app.route('/otolaryngology')
def otolaryngology():
    return render_template('otolaryngology.html')


@app.route('/eye')
def eye():
    return render_template('eye.html')


@app.route('/teeth')
def teeth():
    return render_template('teeth.html')


@app.route('/emergency')
def emergency():
    return render_template('emergency.html')


if __name__ == '__main__':
    app.run(debug=True)
