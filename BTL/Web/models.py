from Web import db
from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey, DateTime, Float, Numeric
from enum import Enum as UserEnum
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.orm import relationship


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, autoincrement=True, primary_key=True)


class UserRole(UserEnum):
    ADMIN = 1
    EMPLOYEE = 2
    USER = 3


class Gender(UserEnum):
    MALE = 1
    FEMALE = 2
    OTHERS = 3


class Position(UserEnum):
    DOCTOR = 1
    NURSE = 2
    MANAGER = 3
    CASHIER = 4


class City(BaseModel):
    __tablename__ = 'city'

    name = Column(String(50), default="--Chọn--")
    district = relationship('District', backref='city', lazy=True)
    user = relationship('User', backref='city', lazy=True)

    def __str__(self):
        return self.name


class District(BaseModel):
    __tablename__ = "district"

    city_id = Column(Integer, ForeignKey(City.id), nullable=False, primary_key=True)
    name = Column(String(50), default="--Chọn--")
    province = relationship('Ward', backref='district', lazy=True)
    user = relationship('User', backref='district', lazy=True)

    def __str__(self):
        return self.name


class Ward(BaseModel):
    __tablename__ = "ward"

    district_id = Column(Integer, ForeignKey(District.id), nullable=False, primary_key=True)
    name = Column(String(50), default="--Chọn--")
    user = relationship('User', backref='ward', lazy=True)

    def __str__(self):
        return self.name


class User(BaseModel, UserMixin):
    __tablename__ = 'user'

    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    active = Column(Boolean, default=False)
    email = Column(String(100), nullable=False)
    joined_date = Column(DateTime, default=datetime.now())
    avatar = Column(String(100))
    date_of_birth = Column(DateTime, nullable=False)
    gender = Column(Enum(Gender), default=Gender.MALE)
    address = Column(String(50))
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    city_id = Column(Integer, ForeignKey(City.id))
    district_id = Column(Integer, ForeignKey(District.id))
    ward_id = Column(Integer, ForeignKey(Ward.id))
    user_position = Column(Enum(Position))

    def __str__(self):
        return self.name


class Cashier(User):
    __tablename__ = 'cashier'

    user_id = Column(Integer, ForeignKey(User.id), nullable=False, primary_key=True, unique=True)
    receipts = relationship('Receipt', backref='cashier', lazy=True)

    def __str__(self):
        return self.name


class Doctor(User):
    __tablename__ = 'doctor'

    user_id = Column(Integer, ForeignKey(User.id), nullable=False, primary_key=True, unique=True)
    toathuoc = relationship('ToaThuoc', backref='doctor', lazy=True)
    phieukham = relationship('PhieuKham', backref='doctor', lazy=True)

    def __str__(self):
        return self.name


class Nurse(User):
    __tablename__ = 'nurse'

    user_id = Column(Integer, ForeignKey(User.id), nullable=False, primary_key=True, unique=True)
    danhsachkham = relationship('DanhSachKham', backref='nurse', lazy=True)

    def __str__(self):
        return self.name


class Manager(User):
    __tablename__ = 'manager'

    user_id = Column(Integer, ForeignKey(User.id), nullable=False, primary_key=True, unique=True)
    rule_id = relationship('Rule', backref='manager', lazy=True)
    is_supervisor = Column(Boolean)

    def __str__(self):
        return self.name


class Guest(User):
    __tablename__ = 'guest'

    user_id = Column(Integer, ForeignKey(User.id), nullable=False, primary_key=True, unique=True)
    last_visited = Column(DateTime)
    appointment = relationship('Appointment', backref='guest', lazy=True)
    toathuoc = relationship('ToaThuoc', backref='guest', lazy=True)
    phieukham = relationship('PhieuKham', backref='guest', lazy=True)
    receipts = relationship('Receipt', backref='guest', lazy=True)
    guest_danhSach = relationship('Guest_DanhSach', backref='guest', lazy=True)

    def __str__(self):
        return self.name


class DanhSachKham(BaseModel):
    __tablename__ = 'danhsachkham'

    nurse_id = Column(Integer, ForeignKey(Nurse.user_id), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    details = relationship('Guest_DanhSach', backref='danhsachkham', lazy=True)


class Guest_DanhSach(db.Model):
    guest_id = Column(Integer, ForeignKey(Guest.user_id), nullable=False, primary_key=True)
    danhsachkham_id = Column(Integer, ForeignKey(DanhSachKham.id), nullable=False, primary_key=True)


class PhieuKham(BaseModel):
    __tablename__ = 'phieukham'

    doctor_id = Column(Integer, ForeignKey(Doctor.user_id), nullable=False, primary_key=True)
    guest_id = Column(Integer, ForeignKey(Guest.user_id), nullable=False, primary_key=True)
    created_date = Column(DateTime, default=datetime.now())
    symptom = Column(String(100), nullable=False)
    diagnose_disease = Column(String(100), nullable=False)
    toathuoc = relationship('ToaThuoc', backref='phieukham', lazy=False, uselist=False)


class Category(BaseModel):
    __tablename__ = 'category'

    name = Column(String(50), nullable=False)
    medicine = relationship('Medicine', backref='category', lazy=False)

    def __str__(self):
        return self.name


class Medicine(BaseModel):
    __tablename__ = 'medicine'

    name = Column(String(50), nullable=False)
    description = Column(String(255))
    price = Column(Integer, nullable=False, default=0)
    image = Column(String(100))
    active = Column(Boolean, default=True)
    unit = Column(String(50), nullable=False, default='Vien')
    created_date = Column(DateTime, default=datetime.now())
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    chitiet_toathuoc = relationship('ChiTietToaThuoc', backref='medicine', lazy=True)
    detail = relationship('ReceiptDetail', backref='medicine', lazy=True)

    def __str__(self):
        return self.name


class Appointment(BaseModel):
    __tablename__ = 'appointment'

    guest_id = Column(Integer, ForeignKey(Guest.user_id), nullable=False, primary_key=True)
    phone_number = Column(Float, nullable=False)
    created_date = Column(DateTime, nullable=False)
    ID_card = Column(Float, default=0)


class Rule(BaseModel):
    __tablename__ = 'rule'

    manager_id = Column(Integer, ForeignKey(Manager.user_id), nullable=False, primary_key=True)
    medical_expense = Column(Integer, nullable=False, default=100000)
    patient = Column(Integer, nullable=False, default=30)


class ToaThuoc(BaseModel):
    __tablename__ = 'toathuoc'

    doctor_id = Column(Integer, ForeignKey(Doctor.user_id), nullable=False, primary_key=True)
    guest_id = Column(Integer, ForeignKey(Guest.user_id), nullable=False, primary_key=True)
    phieukham_id = Column(Integer, ForeignKey(PhieuKham.id), nullable=False, unique=True)
    receipt = relationship('Receipt', backref='toathuoc', lazy=True)
    chitiet_toathuoc = relationship('ChiTietToaThuoc', backref='toathuoc', lazy=True)
    created_date = Column(DateTime, default=datetime.now())


class ChiTietToaThuoc(db.Model):
    toathuoc_id = Column(Integer, ForeignKey(ToaThuoc.id), nullable=False, primary_key=True)
    medicine_id = Column(Integer, ForeignKey(Medicine.id), nullable=False, primary_key=True)
    quantity = Column(Integer, default=0)
    how_to_use = Column(String(50), nullable=False)


class Receipt(BaseModel):
    __tablename__ = 'receipt'

    cashier_id = Column(Integer, ForeignKey(Cashier.user_id), nullable=False, primary_key=True)
    guest_id = Column(Integer, ForeignKey(Guest.user_id), nullable=False, primary_key=True)
    toathuoc_id = Column(Integer, ForeignKey(ToaThuoc.id), nullable=False, primary_key=True, unique=True)
    created_date = Column(DateTime, default=datetime.now())
    details = relationship('ReceiptDetail', backref='receipt', lazy=True)
    medical_expense = Column(Integer, nullable=False, default=100000)


class ReceiptDetail(db.Model):
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False, primary_key=True)
    medicine_id = Column(Integer, ForeignKey(Medicine.id), nullable=False, primary_key=True)
    quantity = Column(Integer, default=0)
    unit_price = Column(Integer, default=0)


if __name__ == '__main__':
    db.create_all()
    # c = Category(name="Thuốc giảm đâu, hạ sốt")
    # c1 = Category(name="Thuốc giải độc")
    # c2 = Category(name="Thuốc kháng sinh")
    # c3 = Category(name="Thuốc từ thiên")
    # c4 = Category(name="Thuốc dị ứng")
    # c5 = Category(name="Thuốc gây tê, mê")
    # c6 = Category(name="Thuốc điều trị ký sinh trùng")
    # c7 = Category(name="Thuốc tim mạch")
    # db.session.add(c)
    # db.session.add(c1)
    # db.session.add(c2)
    # db.session.add(c3)
    # db.session.add(c4)
    # db.session.add(c5)
    # db.session.add(c6)
    # db.session.add(c7)
    # medicines = [{
    #     "name": "Panadol",
    #     "description": "Thuốc giảm đau, hạ sốt",
    #     "price": 20000,
    #     "image": "images/Thuốc giảm đau, hạ sốt/panadol.jpg",
    #     "category_id": 1
    # }, {
    #     "name": "loratadin",
    #     "description": "Thuốc chống dị ứng",
    #     "price": 100000,
    #     "image": "images/Thuốc chống dị ứng/loratadin.jpg",
    #     "category_id": 4
    # }, {
    #     "name": "deferoxamin",
    #     "description": "Thuốc giải độc",
    #     "price": 50000,
    #     "image": "images/Thuốc giải độc/deferoxamin.jpg",
    #     "category_id": 2
    # }, {
    #     "name": "penicillin",
    #     "description": "Thuốc kháng sinh",
    #     "price": 50000,
    #     "image": "images/Thuốc kháng sinh/penicillin.jpg",
    #     "category_id": 3
    # }, {
    #     "name": "aloe vera",
    #     "description": "Thuốc từ thiên nhiên",
    #     "price": 50000,
    #     "image": "images/Thuốc từ thiên nhiên/aloe vera.jpg",
    #     "category_id": 3
    # }]
    # for p in medicines:
    #     med = Medicine(name=p['name'], price=p['price'], image=p['image'],
    #                    description=p['description'], category_id=p['category_id'])
    #     db.session.add(med)
    # city = City(name='TP.HCM')
    # db.session.add(city)
    # district = District(city_id=1, name='Quận 3')
    # db.session.add(district)
    # pro = Ward(district_id=1, name='Phường Võ Thị Sáu')
    # db.session.add(pro)
    u = User(name="admin", username="admin2", password="d9b1d7db4cd6e70935368a1efb10e377", email="admin2@gmail.com",
             date_of_birth="2001/1/11.", user_role=UserRole.ADMIN, user_position=Position.DOCTOR)
    db.session.add(u)
    db.session.commit()
