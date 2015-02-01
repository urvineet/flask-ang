from collections import defaultdict
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import and_, or_
from model.declare import User, Contact, Contact_User, engine, Base


class GetSession():

    def __init__(self):
        """
        Service Class  and View manager
        """
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def add_user(self, user):
        return self.__add(User(username=user))

    def add_contact(self, phone, username, contact_name):
        return self.__add(Contact(phone=phone, username=username, contact_name=contact_name))

    def add_contact_with_user_ref(self, username, phone):
        return self.__add(Contact_User(phone=phone, username=username))


    def __add(self, input_data):
        try:
            self.session.add(input_data)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            return False

    def del_user(self, username):

        return self.__del(self.session.query(User).filter(User.username == username).first())

    def del_contact(self, username, contact_name, phone):
        try:
            print username, contact_name, phone
            return self.__del(
                self.session.query(Contact).filter(
                    and_(Contact.username == username, Contact.phone == phone, Contact.contact_name == contact_name)).first())
        except Exception as e:
            print e


    def __del(self, i):
        try:
            self.session.delete(i)
            self.session.commit()
            return True
        except Exception as e:
            print e
            return False

    def get_list_of_contact(self, user):
        contact_number = []
        list_number = defaultdict(list)
        for i in self.session.query(Contact).filter(Contact.username == user).all():

            contact_number.append(i.phone)
            list_number[i.phone].append(i.contact_name)
        print(contact_number)
        share = defaultdict(list)
        for i in self.session.query(Contact_User).filter(Contact_User.phone.in_(contact_number)).filter(Contact_User.username != user).all():
            print i.phone,i.username
            share[i.phone].append(i.username)
        final = {}
        for i in contact_number:
            print list_number[i] ,share[i]
            final[i] = ({"name": list_number[i], "share": share[i]})

        return final

    def get_user_list(self):
        list = []
        for i in self.session.query(User).all():
            list.append(i.username)
        return {'user_list': list}




