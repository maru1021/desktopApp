from sqlalchemy.exc import IntegrityError
from tkinter import messagebox
from db_access import session
from models.department import Department
from models.employee import Employee
from components.show_notification import show_notification
from components.create_modal import create_modal
from views.PageManager import PageManager
from valid.valids import validate_required

class DepartmentManager(PageManager):
    title = "部署管理"
    columns = ("ID", "部署名")
    validation_rules = {
        "部署名": [validate_required],
    }

    def refresh(self, search_text, tree):
        for row in tree.get_children():
            tree.delete(row)
        query = session.query(Department).filter(Department.name.like(f"%{search_text}%"))
        for department in query.all():
            tree.insert("", "end", values=(department.id, department.name))

    def register(self, values):
        try:
            new_department = Department(name=values["部署名"])
            session.add(new_department)
            session.commit()
            self.refresh("", self.tree)
            show_notification(self.root, "登録されました")
        except IntegrityError:
            session.rollback()
            show_notification(self.root, "部署名が重複しています")

    def edit(self, selected_item):
        department_id, name = self.tree.item(selected_item)["values"]

        def update_department(values):
            try:
                department = session.query(Department).filter_by(id=department_id).first()
                department.name = values["部署名"]
                session.commit()
                self.refresh("", self.tree)
                show_notification(self.root, "更新されました")
            except Exception as e:
                session.rollback()
                show_notification(self.root, f"予期しないエラー: {e}")

        fields={"部署名": name}
        create_modal(self.root, "部署編集", fields, self.validation_rules, on_confirm=update_department)

    def delete(self, item_id):
        linked_employees = session.query(Employee).filter_by(department_id=item_id).count()
        if linked_employees > 0:
            show_notification(self.root, "この部署には従業員が紐づいているため削除できません")
            return

        if messagebox.askyesno("確認", "この部署を削除しますか？", parent=self.root):
            session.query(Department).filter_by(id=item_id).delete()
            session.commit()
            self.refresh("", self.tree)
            show_notification(self.root, "部署が削除されました")

    def show_register_modal(self):
        fields={"部署名": ""}
        create_modal(self.root, "部署登録", fields, self.validation_rules, on_confirm=self.register)

    def show_edit_modal(self, selected_item):
        self.edit(selected_item)
