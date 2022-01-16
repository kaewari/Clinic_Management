from Web import db, app
import hashlib
from Web.models import Category, Medicine, ToaThuoc, ChiTietToaThuoc, \
    ReceiptDetail, Receipt, Appointment, PhieuKham, DanhSachKham, Rule, User, Guest, Cashier, Doctor, Nurse, Manager, \
    City, UserRole, Guest_DanhSach, District, Ward
from sqlalchemy import func, extract
from flask_login import current_user
from datetime import datetime
import json, os


def check_login(username, password, user_role):
    if username and password:
        password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password),
                                 User.user_role.__eq__(user_role)).first()


def get_doctor_by_id(doctor_id):
    return Doctor.query.get(doctor_id)


def get_cashier_by_id(cashier_id):
    return Cashier.query.get(cashier_id)


def get_nurse_by_id(nurse_id):
    return Nurse.query.get(nurse_id)


def get_medicine_by_id(medicine_id):
    return Medicine.query.get(medicine_id)


def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_receipt_detail_by_id(receipt_id=None, year=None, month=None, day=None, from_date=None, to_date=None):
    if receipt_id is None:
        return None
    else:
        q = db.session.query(ReceiptDetail.receipt_id, ReceiptDetail.medicine_id, ReceiptDetail.quantity,
                             ReceiptDetail.unit_price, Receipt.created_date) \
            .join(Receipt, Receipt.id.__eq__(ReceiptDetail.receipt_id))
        if receipt_id:
            q = q.filter(ReceiptDetail.receipt_id.__eq__(receipt_id))
        if year:
            q = q.filter(extract('year', Receipt.created_date).__eq__(year))
        if month:
            q = q.filter(extract('month', Receipt.created_date).__eq__(month))
        if day:
            q = q.filter(extract('day', Receipt.created_date).__eq__(day))
        if from_date:
            q = q.filter(Receipt.created_date.__ge__(from_date))
        if to_date:
            q = q.filter(Receipt.created_date.__le__(to_date))
        return q.all()


def get_chitiet_toathuoc_by_id(toathuoc_id=None):
    q = db.session.query(ChiTietToaThuoc.toathuoc_id, ChiTietToaThuoc.medicine_id, ChiTietToaThuoc.quantity,
                         ChiTietToaThuoc.how_to_use)
    if toathuoc_id:
        q = q.filter(ChiTietToaThuoc.toathuoc_id.__eq__(toathuoc_id))
    return q.all()


def get_guest_by_id(guest_id):
    return Guest.query.get(guest_id)


def get_manager_by_id(manager_id):
    return Manager.query.get(manager_id)


def category_stats():
    return db.session.query(Category.id, Category.name, func.count(Medicine.id)) \
        .join(Medicine, Category.id.__eq__(Medicine.category_id), isouter=True) \
        .group_by(Category.id, Category.name).all()


def medicine_stats(year=None, month=None, day=None, kw=None, from_date=None, to_date=None):
    q = db.session.query(Medicine.id, Medicine.name,
                         func.sum(ReceiptDetail.quantity * ReceiptDetail.unit_price),
                         func.count(ReceiptDetail.medicine_id),
                         func.sum(ReceiptDetail.quantity),
                         extract('day', Receipt.created_date),
                         extract('month', Receipt.created_date),
                         extract('year', Receipt.created_date)) \
        .join(ReceiptDetail, ReceiptDetail.medicine_id.__eq__(Medicine.id), isouter=True) \
        .join(Receipt, Receipt.id.__eq__(ReceiptDetail.receipt_id))
    if year:
        q = q.filter(extract('year', Receipt.created_date).__eq__(year))
    if month:
        q = q.filter(extract('month', Receipt.created_date).__eq__(month))
    if day:
        q = q.filter(extract('day', Receipt.created_date).__eq__(day))
    if kw:
        q = q.filter(Medicine.name.contains(kw))
    if from_date:
        q = q.filter(Receipt.created_date.__ge__(from_date))
    if to_date:
        q = q.filter(Receipt.created_date.__le__(to_date))
    return q.group_by(Medicine.id).all()


def medicine_month_stats(year=None, month=None, day=None, from_date=None, to_date=None):
    q = db.session.query(extract('day', Receipt.created_date),
                         extract('month', Receipt.created_date),
                         extract('year', Receipt.created_date),
                         func.sum(ReceiptDetail.quantity * ReceiptDetail.unit_price),
                         func.count(Receipt.id),
                         func.count(Receipt.id) / func.sum(ReceiptDetail.quantity * ReceiptDetail.unit_price))
    if year:
        q = q.filter(extract('year', Receipt.created_date).__eq__(year))
    if month:
        q = q.filter(extract('month', Receipt.created_date).__eq__(month))
    if day:
        q = q.filter(extract('day', Receipt.created_date).__eq__(day))
    if from_date:
        q = q.filter(Receipt.created_date.__ge__(from_date))
    if to_date:
        q = q.filter(Receipt.created_date.__le__(to_date))
    return q.group_by(Receipt.id).all()


def create_user(name, username, password, gender, city=None, district=None, date_of_birth=None, ward=None, email=None, avatar=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    if avatar:
        avatar = avatar
    else:
        avatar = 'https://res.cloudinary.com/dt8p4xhzz/image/upload/v1641660925/akew2xsulpu7xryxjhdl.jpg'

    user = Guest(name=name.strip(),
                 username=username.strip(),
                 password=password,
                 date_of_birth=date_of_birth,
                 gender=gender,
                 email=email.strip() if email else email,
                 avatar=avatar)
    db.session.add(user)
    if city:
        user.city_id = city
    if district:
        user.district_id = district
    if ward:
        user.ward_id = ward
    try:
        db.session.commit()
    except:
        return False
    else:
        return True


def change_new_info(name=None, username=None, gender=None, active=None, city=None, district=None, ward=None, email=None, avatar=None):
    user = User.query.get(current_user.id)
    if name:
        user.name = name
    if username:
        user.username = username
    if email:
        user.email = email
    if gender:
        user.gender = gender
    if active:
        user.active = active
    if district:
        user.district_id = district
    if ward:
        user.ward_id = ward
    if city:
        user.city_id = city
    if avatar:
        user.avatar = avatar
    db.session.add(user)
    try:
        db.session.commit()
    except:
        return False
    else:
        return True


def change_new_password(new_password):
    user = User.query.get(current_user.id)
    user.password = hashlib.md5(new_password.strip().encode('utf-8')).hexdigest()
    db.session.add(user)
    try:
        db.session.commit()
    except:
        return False
    else:
        return True


def create_appointment(phone_number, created_date, ID_card):
    user = Appointment(guest_id=current_user.id,
                       created_date=created_date,
                       phone_number=phone_number.strip(),
                       ID_card=ID_card.strip())
    db.session.add(user)

    try:
        db.session.commit()
    except:
        return False
    else:
        return True


def load_guest(kw=None):
    q = db.session.query(Guest.id, Guest.name, Guest.avatar)
    if kw:
        q = q.filter(Guest.name.contains(kw))
    return q.all()


def load_employee():
    return User.query.filter(User.user_role != UserRole.USER).all()


def load_appointment(kw=None, day=None, month=None, year=None):
    q = db.session.query(Appointment.guest_id, Guest.name, Appointment.phone_number,
                         Appointment.ID_card, Appointment.created_date). \
        join(Appointment, Appointment.guest_id.__eq__(Guest.id))
    if kw:
        q = q.filter(Appointment.name.contains(kw))
    if day:
        q = q.filter(extract('day', Appointment.created_date).__eq__(day))
    if month:
        q = q.filter(extract('month', Appointment.created_date).__eq__(month))
    if year:
        q = q.filter(extract('year', Appointment.created_date).__eq__(year))
    return q.all()


def load_city():
    return City.query.all()


def load_district():
    return District.query.all()


def load_ward():
    return Ward.query.all()


def load_manager():
    return Manager.query.all()


def load_tien_kham():
    return Rule.query.all()


def load_receipt():
    return Receipt.query.all()


def load_receipt_detail():
    return ReceiptDetail.query.all()


def load_prescription():
    return ToaThuoc.query.all()


def load_detail_prescription():
    return ChiTietToaThuoc.query.all()


def load_categories():
    return Category.query.all()


def load_form(kw=None):
    q = PhieuKham.query.all()
    if kw:
        q = PhieuKham.filter(PhieuKham.user_id.name.contains(kw))
    return q


def load_medicine(kw=None, from_price=None, to_price=None, cate_id=None):
    medicine = Medicine.query.filter(Medicine.active.__eq__(True))

    if cate_id:
        medicine = medicine.filter(Medicine.category_id.__eq__(cate_id))

    if kw:
        medicine = medicine.filter(Medicine.name.contains(kw))

    if from_price:
        medicine = medicine.filter(Medicine.price.__ge__(from_price))

    if to_price:
        medicine = medicine.filter(Medicine.price.__le__(to_price))

    return medicine.all()


def add_receipt(cart, medical_expense, guest_id, toathuoc_id):
    if cart:
        receipt = Receipt(cashier_id=current_user.id,
                          medical_expense=medical_expense,
                          guest_id=guest_id, toathuoc_id=toathuoc_id)
        db.session.add(receipt)

        for c in cart.values():
            detail = ReceiptDetail(receipt=receipt,
                                   medicine_id=c['id'],
                                   quantity=c['quantity'],
                                   unit_price=c['price'])
            db.session.add(detail)

        db.session.commit()


def count_cart(cart):
    total_quantity, total_amount = 0, 0

    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_amount += c['quantity'] * c['price']

    return {
        'total_quantity': total_quantity,
        'total_amount': total_amount
    }


def count(form):
    total_quantity, total_amount = 0, 0

    if form:
        for pre in form.values():
            total_quantity += pre['quantity']

    return {
        'total_quantity': total_quantity,
        'total_amount': total_amount
    }


def add_medical_form(form, guest_id, symptom, diagnose_disease, how_to_use):
    if form:
        medical_form = PhieuKham(doctor_id=current_user.id, guest_id=guest_id,
                                 symptom=symptom, diagnose_disease=diagnose_disease)
        db.session.add(medical_form)
        db.session.commit()
        prescription = ToaThuoc(doctor_id=current_user.id, guest_id=guest_id,
                                phieukham_id=medical_form.id)
        db.session.add(prescription)
        db.session.commit()
        for c in form.values():
            detail = ChiTietToaThuoc(toathuoc_id=prescription.id,
                                     medicine_id=c['id'],
                                     quantity=c['quantity'],
                                     how_to_use=how_to_use)
            db.session.add(detail)

        db.session.commit()


def select_max_medicine_id():
    max_id = ToaThuoc.query.filter(func.count(ToaThuoc.id))
    return max_id


def select_max_guest_id():
    max_id = User.query.filter(func.count(User.user_role.__eq__('USER')))
    return max_id


def find_guest_in_form(guest_id=None, day=None, month=None, year=None):
    if guest_id is None:
        return None
    else:
        q = db.session.query(Guest.name, PhieuKham.created_date, PhieuKham.symptom,
                             PhieuKham.diagnose_disease). \
            join(Guest, Guest.id.__eq__(PhieuKham.guest_id))
        if guest_id:
            q = q.filter(PhieuKham.guest_id.__eq__(guest_id))
        if year:
            q = q.filter(extract('year', PhieuKham.created_date).__eq__(year))
        if month:
            q = q.filter(extract('month', PhieuKham.created_date).__eq__(month))
        if day:
            q = q.filter(extract('day', PhieuKham.created_date).__eq__(day))
        return q.all()


def find_toathuoc_in_form(guest_id=None, day=None, month=None, year=None):
    if guest_id is None:
        return None
    else:
        q = db.session.query(Medicine.name, Medicine.unit, ChiTietToaThuoc.quantity, ChiTietToaThuoc.how_to_use). \
            join(Medicine, Medicine.id.__eq__(ChiTietToaThuoc.medicine_id))
        if guest_id:
            q = q.filter(PhieuKham.guest_id.__eq__(guest_id))
        if year:
            q = q.filter(extract('year', PhieuKham.created_date).__eq__(year))
        if month:
            q = q.filter(extract('month', PhieuKham.created_date).__eq__(month))
        if day:
            q = q.filter(extract('day', PhieuKham.created_date).__eq__(day))
        return q.all()


def get_receipt_in_receipt_info(guest_id=None, year=None, month=None, day=None):
    if guest_id is None:
        return None
    else:
        q = db.session.query(Guest.name, Receipt.created_date, Receipt.medical_expense,
                             ReceiptDetail.quantity * ReceiptDetail.unit_price,
                             ReceiptDetail.quantity * ReceiptDetail.unit_price + Receipt.medical_expense). \
            join(Receipt, Receipt.guest_id.__eq__(Guest.id)). \
            join(ReceiptDetail, ReceiptDetail.receipt_id.__eq__(Receipt.id))
        if guest_id:
            q = q.filter(Receipt.guest_id.__eq__(guest_id))
        if year:
            q = q.filter(extract('year', Receipt.created_date).__eq__(year))
        if month:
            q = q.filter(extract('month', Receipt.created_date).__eq__(month))
        if day:
            q = q.filter(extract('day', Receipt.created_date).__eq__(day))
        return q.group_by(Receipt.id).all()


def create_list():
    q = DanhSachKham(nurse_id=current_user.id)
    db.session.add(q)
    try:
        db.session.commit()
    except:
        return False
    else:
        return True


def save_danhsachkham_info(guest_id, danhsachkham_id):
    p = Guest_DanhSach(danhsachkham_id=danhsachkham_id, guest_id=guest_id)
    db.session.add(p)
    db.session.commit()


def show_list(day=None):
    q = db.session.query(Guest.name, Guest.gender, Guest.date_of_birth, Guest.address, DanhSachKham.created_date). \
        join(Guest_DanhSach, Guest_DanhSach.danhsachkham_id.__eq__(DanhSachKham.id)). \
        join(Guest, Guest.id.__eq__(Guest_DanhSach.guest_id))
    if day:
        q = q.filter(extract('day', DanhSachKham.created_date).__eq__(day))
    return q.all()


def count_patient(day=datetime.now().day):
    q = db.session.query(func.count(Guest_DanhSach.guest_id)). \
        join(DanhSachKham, DanhSachKham.id.__eq__(Guest_DanhSach.danhsachkham_id))
    if day:
        q = q.filter(extract('day', DanhSachKham.created_date).__eq__(day))
    return q.group_by(Guest_DanhSach.guest_id).all()


def count_list():
    q = db.session.query(DanhSachKham.id). \
        order_by(-DanhSachKham.id)
    return q.all()


def delete_list(danhsachkham_id):
    q = DanhSachKham.query.get(danhsachkham_id)
    db.session.delete(q)
    db.session.commit()
