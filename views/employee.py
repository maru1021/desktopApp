from sqlalchemy.exc import IntegrityError
from tkinter import messagebox
from db_access import session
from models.department import Department
from models.employee import Employee
from components.show_notification import show_notification
from components.create_modal import create_modal
from views.PageManager import PageManager

class EmployeeManager(PageManager):
    title = "従業員管理"
    columns = ("ID", "名前", "メールアドレス", "部署")
    model = Employee

    def refresh(self, search_text, tree):
        for row in tree.get_children():
            tree.delete(row)
        query = session.query(Employee).join(Department).filter(
            (Employee.name.like(f"%{search_text}%")) |
            (Employee.email.like(f"%{search_text}%")) |
            (Department.name.like(f"%{search_text}%"))
        )
        for emp in query.all():
            tree.insert("", "end", values=(emp.id, emp.name, emp.email, emp.department.name if emp.department else ""))

    def register(self, values):
        department_name = values.get("部署")
        department = session.query(Department).filter_by(name=department_name).first()
        try:
            new_employee = Employee(name=values["名前"], email=values["メールアドレス"], department=department)
            session.add(new_employee)
            session.commit()
            self.refresh("", self.tree)
            show_notification(self.root, "登録されました")
        except IntegrityError:
            session.rollback()
            show_notification(self.root, "メールアドレスが重複しています")
        except Exception as e:
            session.rollback()
            show_notification(self.root, f"予期しないエラー: {e}")

    def edit(self, selected_item):
        employee_id, name, email, department_name = self.tree.item(selected_item)["values"]

        def update_employee(values):
            try:
                emp = session.query(Employee).filter_by(id=employee_id).first()
                emp.name = values["名前"]
                emp.email = values["メールアドレス"]
                emp.department = session.query(Department).filter_by(name=values.get("部署")).first()
                session.commit()
                self.refresh("", self.tree)
                show_notification(self.root, "更新されました")
            except IntegrityError:
                session.rollback()
                show_notification(self.root, "メールアドレスが重複しています")
            except Exception as e:
                session.rollback()
                show_notification(self.root, f"予期しないエラー: {e}")

        create_modal(self.root, "従業員編集", fields={"名前": name, "メールアドレス": email, "部署": department_name},
                     department_dropdown=True, on_confirm=update_employee)

    def delete(self, item_id):
        if messagebox.askyesno("確認", "この従業員を削除しますか？", parent=self.root):
            session.query(Employee).filter_by(id=item_id).delete()
            session.commit()
            self.refresh("", self.tree)
            show_notification(self.root, "削除されました")

    def show_register_modal(self):
        create_modal(self.root, "従業員登録", {"名前": "", "メールアドレス": "", "部署": ""},
                     department_dropdown=True, on_confirm=self.register)

    def show_edit_modal(self, selected_item):
        self.edit(selected_item)