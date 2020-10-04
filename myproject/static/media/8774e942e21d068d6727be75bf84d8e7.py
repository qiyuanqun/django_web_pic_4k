import xlrd
import xlwt
import pymysql
from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont
import tkinter.messagebox as messagebox


# 数据库操作的工具类
class PyMySQLUtils:
    # 获取连接
    def __init__(self):
        # 打开数据库连接
        self.db = pymysql.connect("localhost", "root", "123456", "school")
        # 使用cursor()方法获取操作游标
        self.cursor = self.db.cursor()

    # 查询获取多条数据
    def fetchall(self, sql):
        # 使用execute()方法执行SQL语句
        self.cursor.execute(sql)
        # 使用fetchall()方法获取多条数据
        results = self.cursor.fetchall()
        return results

    # 查询获取单条数据
    def fetchone(self, sql):
        # 使用execute()方法执行SQL语句
        self.cursor.execute(sql)
        # 使用fetchone()方法获取单条数据
        result = self.cursor.fetchone()
        return result

    # 添加删除更新操作
    def execute(self, sql):
        try:
            # 使用execute()方法执行SQL语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
            print("数据库操作成功！")
        except:
            # 发生错误时回滚
            self.db.rollback()
            print("数据库连接失败！")

    # 关闭连接
    def close(self):
        # 关闭游标
        self.cursor.close()
        # 关闭数据库连接
        self.db.close()


# 开始界面
class StartMenu:
    def __init__(self, parent_window):
        parent_window.destroy()
        self.window = Tk()
        self.window.title("学生成绩管理系统-教师版")
        self.window.geometry("500x500")
        self.window.resizable(0, 0)
        Label(self.window, text="学生成绩管理系统", font=("宋体", 20)).pack(pady=100)
        Button(self.window, text="教师注册", font=tkFont.Font(size=16), command=lambda: TeacherRegister(self.window),
               width=30, height=2, fg="white", bg="gray", activeforeground="white", activebackground="black").pack()
        Button(self.window, text="教师登录", font=tkFont.Font(size=16), command=lambda: TeacherLogin(self.window), width=30,
               height=2, fg="white", bg="gray", activeforeground="white", activebackground="black").pack()
        Button(self.window, text="退出系统", font=tkFont.Font(size=16), command=self.window.destroy, width=30, height=2,
               fg="white", bg="gray", activeforeground="white", activebackground="black").pack()
        self.window.mainloop()


# 教师注册界面
class TeacherRegister:
    def __init__(self, parent_window):
        parent_window.destroy()
        self.window = Tk()
        self.window.title("学生成绩管理系统-教师版")
        self.window.geometry("500x500")
        self.window.resizable(0, 0)
        Label(self.window, text="欢迎教师注册", font=("宋体", 20)).pack(pady=100)
        Label(self.window, text="输入账号：", font=tkFont.Font(size=14)).place(x=100, y=200)
        self.my_username = Entry(self.window, width=20, font=tkFont.Font(size=14), bg='Ivory')
        self.my_username.place(x=200, y=200)
        Label(self.window, text="输入密码：", font=tkFont.Font(size=14)).place(x=100, y=250)
        self.my_password = Entry(self.window, width=20, font=tkFont.Font(size=14), bg='Ivory', show='*')
        self.my_password.place(x=200, y=250)
        Label(self.window, text="确认密码：", font=tkFont.Font(size=14)).place(x=100, y=300)
        self.re_password = Entry(self.window, width=20, font=tkFont.Font(size=14), bg='Ivory', show='*')
        self.re_password.place(x=200, y=300)
        Button(self.window, text="确定", width=8, font=tkFont.Font(size=12), command=self.register).place(x=200, y=350)
        Button(self.window, text="返回", width=8, font=tkFont.Font(size=12), command=self.back).place(x=330, y=350)
        self.window.protocol("WM_DELETE_WINDOW", self.back)
        self.window.mainloop()

    def register(self):
        utils = PyMySQLUtils()
        result = utils.fetchone("SELECT * FROM teacher_login WHERE username = '%s'" % self.my_username.get())
        if self.my_username.get() == "" or self.my_password.get() == "" or self.re_password.get() == "":
            messagebox.showerror(title="showerror", message="注册失败！注册信息不完整！")
        elif self.my_password.get() != self.re_password.get():
            messagebox.showerror(title="showerror", message="注册失败！两次密码不相同！")
        elif result:
            messagebox.showerror(title="showerror", message="注册失败！该账号已被注册过！")
        else:
            print(self.my_username.get())
            print()
            utils.execute("INSERT INTO teacher_login(username, password) VALUES('%s', '%s')" % (
                self.my_username.get(), self.my_password.get()))
            utils.close()
            messagebox.showinfo(title="showinfo", message="注册成功！欢迎您登录使用！")
            TeacherLogin(self.window)

    def back(self):
        StartMenu(self.window)


# 教师登录界面
class TeacherLogin:
    def __init__(self, parent_window):
        parent_window.destroy()
        self.window = Tk()
        self.window.title("学生成绩管理系统-教师版")
        self.window.geometry("500x500")
        self.window.resizable(0, 0)
        Label(self.window, text="欢迎教师登录", font=("宋体", 20)).pack(pady=100)
        Label(self.window, text="账号：", font=tkFont.Font(size=14)).place(x=100, y=200)
        self.my_username = Entry(self.window, width=20, font=tkFont.Font(size=14), bg='Ivory')
        self.my_username.place(x=170, y=200)
        Label(self.window, text="密码：", font=tkFont.Font(size=14)).place(x=100, y=250)
        self.my_password = Entry(self.window, width=20, font=tkFont.Font(size=14), bg='Ivory', show='*')
        self.my_password.place(x=170, y=250)
        Button(self.window, text="确定", width=8, font=tkFont.Font(size=12), command=self.login).place(x=170, y=300)
        Button(self.window, text="返回", width=8, font=tkFont.Font(size=12), command=self.back).place(x=300, y=300)
        self.window.protocol("WM_DELETE_WINDOW", self.back)
        self.window.mainloop()

    def login(self):
        utils = PyMySQLUtils()
        result = utils.fetchone("SELECT * FROM teacher_login WHERE username = '%s'" % self.my_username.get())
        if self.my_username.get() == "" or self.my_password.get() == "":
            messagebox.showerror(title="showerror", message="登录失败！登录信息不完整！")
        elif result:
            utils.close()
            if self.my_password.get() == result[1]:
                messagebox.showinfo("showinfo", "登录成功！欢迎您使用！")
                TeacherMenu(self.window)
            else:
                messagebox.showerror("showerror", "登录失败！输入的密码错误！")
        else:
            messagebox.showerror("showerror", "登录失败！输入的账号有误！")

    def back(self):
        StartMenu(self.window)


# 教师操作界面
class TeacherMenu:
    def __init__(self, parent_window):
        parent_window.destroy()
        self.window = Tk()
        self.window.title("学生成绩管理系统-教师版")
        self.window.resizable(0, 0)
        Label(self.window, text="学生成绩管理系统", font=("宋体", 20)).grid(row=0, column=0, columnspan=2, padx=5, pady=20)

        # 中心区域
        self.frame_center = Frame(width=900, height=500)
        self.frame_center.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
        self.columns = ("学号", "姓名", "院系", "语文成绩", "数学成绩", "英语成绩", "考试平均成绩", "同学互评分", "任课教师评分", "综合测评总分")
        self.tree = ttk.Treeview(self.frame_center, show="headings", height=15, columns=self.columns)
        self.tree.grid(row=0, column=0)
        self.vbar = ttk.Scrollbar(self.frame_center, orient=VERTICAL, command=self.tree.yview)
        self.vbar.grid(row=0, column=1)
        self.tree.configure(yscrollcommand=self.vbar.set)
        self.tree.column("学号", width=80, anchor='center')
        self.tree.column("姓名", width=80, anchor='center')
        self.tree.column("院系", width=80, anchor='center')
        self.tree.column("语文成绩", width=80, anchor='center')
        self.tree.column("数学成绩", width=80, anchor='center')
        self.tree.column("英语成绩", width=80, anchor='center')
        self.tree.column("考试平均成绩", width=80, anchor='center')
        self.tree.column("同学互评分", width=80, anchor='center')
        self.tree.column("任课教师评分", width=80, anchor='center')
        self.tree.column("综合测评总分", width=80, anchor='center')
        self.tree.heading("学号", text="学号")
        self.tree.heading("姓名", text="姓名")
        self.tree.heading("院系", text="院系")
        self.tree.heading("语文成绩", text="语文成绩")
        self.tree.heading("数学成绩", text="数学成绩")
        self.tree.heading("英语成绩", text="英语成绩")
        self.tree.heading("考试平均成绩", text="考试平均成绩")
        self.tree.heading("同学互评分", text="同学互评分")
        self.tree.heading("任课教师评分", text="任课教师评分")
        self.tree.heading("综合测评总分", text="综合测评总分")

        # 左方区域
        self.frame_left = Frame(width=200, height=250)
        self.frame_left.grid(row=2, column=0, sticky=NS)
        self.left_frame = Frame(self.frame_left)
        self.var_sid = StringVar()
        self.var_sname = StringVar()
        self.var_sdept = StringVar()
        self.var_chinese = IntVar()
        self.var_math = IntVar()
        self.var_english = IntVar()
        self.var_classmate_score = IntVar()
        self.var_teacher_score = IntVar()

        Label(self.frame_left, text="学号：", font=("宋体", 10)).grid(row=0, column=0, padx=10, pady=5, sticky=NE)
        Label(self.frame_left, text="姓名：", font=("宋体", 10)).grid(row=1, column=0, padx=10, pady=5, sticky=NE)
        Label(self.frame_left, text="院系：", font=("宋体", 10)).grid(row=2, column=0, padx=10, pady=5, sticky=NE)
        Label(self.frame_left, text="语文成绩：", font=("宋体", 10)).grid(row=3, column=0, padx=10, pady=5, sticky=NE)
        Label(self.frame_left, text="数学成绩：", font=("宋体", 10)).grid(row=4, column=0, padx=10, pady=5, sticky=NE)
        Label(self.frame_left, text="英语成绩：", font=("宋体", 10)).grid(row=5, column=0, padx=10, pady=5, sticky=NE)
        Label(self.frame_left, text="同学互评分：", font=("宋体", 10)).grid(row=7, column=0, padx=10, pady=5, sticky=NE)
        Label(self.frame_left, text="任课教师评分：", font=("宋体", 10)).grid(row=8, column=0, padx=10, pady=5, sticky=NE)

        Entry(self.frame_left, textvariable=self.var_sid, font=("宋体", 10)).grid(row=0, column=1, padx=5, pady=5)
        Entry(self.frame_left, textvariable=self.var_sname, font=("宋体", 10)).grid(row=1, column=1, padx=5, pady=5)
        Entry(self.frame_left, textvariable=self.var_sdept, font=("宋体", 10)).grid(row=2, column=1, padx=5, pady=5)
        Entry(self.frame_left, textvariable=self.var_chinese, font=("宋体", 10)).grid(row=3, column=1, padx=5, pady=5)
        Entry(self.frame_left, textvariable=self.var_math, font=("宋体", 10)).grid(row=4, column=1, padx=5, pady=5)
        Entry(self.frame_left, textvariable=self.var_english, font=("宋体", 10)).grid(row=5, column=1, padx=5, pady=5)
        Entry(self.frame_left, textvariable=self.var_classmate_score, font=("宋体", 10)).grid(row=7, column=1, padx=5, pady=5)
        Entry(self.frame_left, textvariable=self.var_teacher_score, font=("宋体", 10)).grid(row=8, column=1, padx=5, pady=5)

        # 右方区域
        self.frame_right = Frame(width=500, height=250)
        self.frame_right.grid(row=2, column=1)
        Button(self.frame_right, text="清空输入框的内容", width=30, command=self.clear).grid(row=0, column=0, padx=5, pady=5)
        Button(self.frame_right, text="新增学生成绩信息", width=30, command=self.insert).grid(row=1, column=0, padx=5, pady=5)
        Button(self.frame_right, text="修改学生成绩信息", width=30, command=self.update).grid(row=2, column=0, padx=5, pady=5)
        Button(self.frame_right, text="查询学生成绩信息", width=30, command=self.select).grid(row=3, column=0, padx=5, pady=5)
        Button(self.frame_right, text="删除学生成绩信息", width=30, command=self.delete).grid(row=4, column=0, padx=5, pady=5)
        Button(self.frame_right, text="写入到Excel文件", width=30,
               command=lambda: mysql_excel("E:\\PycharmProjects\\StudentScoreManagerSystem\\NewStudentScore.xls")).grid(row=5, column=0, padx=5, pady=5)

        # 定义储存数据的列表
        self.list_sid = []
        self.list_sname = []
        self.list_sdept = []
        self.list_chinese = []
        self.list_math = []
        self.list_english = []
        self.list_average_score = []
        self.list_classmate_score = []
        self.list_teacher_score = []
        self.list_total_score = []

        # 从数据库获取表格内容
        utils = PyMySQLUtils()
        results = utils.fetchall("SELECT * FROM student_score")
        for row in results:
            self.list_sid.append(row[0])
            self.list_sname.append(row[1])
            self.list_sdept.append(row[2])
            self.list_chinese.append(row[3])
            self.list_math.append(row[4])
            self.list_english.append(row[5])
            self.list_average_score.append(row[6])
            self.list_classmate_score.append(row[7])
            self.list_teacher_score.append(row[8])
            self.list_total_score.append(row[9])
        utils.close()

        # 设置表格内容
        for i in range(min(len(self.list_sid), len(self.list_sname), len(self.list_sdept), len(self.list_chinese),
                           len(self.list_math), len(self.list_english), len(self.list_average_score),
                           len(self.list_classmate_score), len(self.list_teacher_score), len(self.list_total_score))):
            self.tree.insert("", i,
                             values=(self.list_sid[i], self.list_sname[i], self.list_sdept[i], self.list_chinese[i],
                                     self.list_math[i], self.list_english[i], self.list_average_score[i],
                                     self.list_classmate_score[i], self.list_teacher_score[i],
                                     self.list_total_score[i]))

        # 绑定函数使表头可排序
        for col in self.columns:
            self.tree.heading(col, text=col, command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))

        # 绑定点击事件
        self.tree.bind('<ButtonRelease-1>', self.tree_click)

        self.window.protocol("WM_DELETE_WINDOW", self.back)
        self.window.mainloop()

    # 点击表头排序
    def tree_sort_column(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l):
            # 根据排序后索引移动
            tv.move(k, '', index)
        # 重写标题，使之成为再点倒序的标题
        tv.heading(col, command=lambda: self.tree_sort_column(tv, col, not reverse))

    # 获取被点击的条目
    def tree_click(self, event):
        row = self.tree.identify_row(event.y)
        row_info = self.tree.item(row, 'values')
        self.var_sid.set(row_info[0])
        self.var_sname.set(row_info[1])
        self.var_sdept.set(row_info[2])
        self.var_chinese.set(row_info[3])
        self.var_math.set(row_info[4])
        self.var_english.set(row_info[5])
        self.var_classmate_score.set(row_info[7])
        self.var_teacher_score.set(row_info[8])

    # 清空输入框的内容
    def clear(self):
        self.var_sid.set("")
        self.var_sname.set("")
        self.var_sdept.set("")
        self.var_chinese.set("")
        self.var_math.set("")
        self.var_english.set("")
        self.var_classmate_score.set("")
        self.var_teacher_score.set("")

    # 添加学生成绩信息
    def insert(self):
        if messagebox.askyesnocancel("askyesnocancel", "是否该添加学生成绩信息？"):
            sid = self.var_sid.get()
            sname = self.var_sname.get()
            sdept = self.var_sdept.get()
            chinese = round(float(self.var_chinese.get()), 2)
            math = round(float(self.var_math.get()), 2)
            english = round(float(self.var_english.get()), 2)
            average_score = round(((chinese + math + english) / 3), 2)
            classmate_score = round(float(self.var_classmate_score.get()), 2)
            teacher_score = round(float(self.var_teacher_score.get()), 2)
            total_score = round((average_score * 0.7 + classmate_score * 0.1 + teacher_score * 0.2), 2)
            if sid in self.list_sid:
                messagebox.showwarning("showwarning", "该学生成绩信息已存在！")
            else:
                utils = PyMySQLUtils()
                utils.execute(
                    f"INSERT INTO student_score VALUES('{sid}', '{sname}', '{sdept}', {chinese}, {math}, {english}, "
                    f"{average_score}, {classmate_score}, {teacher_score}, {total_score})")
                utils.close()
                self.list_sid.append(sid)
                self.list_sname.append(sname)
                self.list_sdept.append(sdept)
                self.list_chinese.append(chinese)
                self.list_math.append(math)
                self.list_english.append(english)
                self.list_average_score.append(average_score)
                self.list_classmate_score.append(classmate_score)
                self.list_teacher_score.append(teacher_score)
                self.list_total_score.append(total_score)
                self.tree.insert('', 'end', values=(sid, sname, sdept, chinese, math, english, average_score,
                                                    classmate_score, teacher_score, total_score))
                self.tree.update()
                messagebox.showinfo("showinfo", "添加学生成绩信息成功！")

    # 修改学生成绩信息
    def update(self):
        if messagebox.askyesnocancel("askyesnocancel", "是否修改该学生成绩信息？"):
            sid = self.var_sid.get()
            sname = self.var_sname.get()
            sdept = self.var_sdept.get()
            chinese = round(float(self.var_chinese.get()), 2)
            math = round(float(self.var_math.get()), 2)
            english = round(float(self.var_english.get()), 2)
            average_score = round(((chinese + math + english) / 3), 2)
            classmate_score = round(float(self.var_classmate_score.get()), 2)
            teacher_score = round(float(self.var_teacher_score.get()), 2)
            total_score = round((average_score * 0.7 + classmate_score * 0.1 + teacher_score * 0.2), 2)
            if sid not in self.list_sid:
                messagebox.showwarning("showwarning", "该学生成绩信息不存在！")
            else:
                utils = PyMySQLUtils()
                utils.execute(
                    f"UPDATE student_score SET sname = '{sname}', sdept = '{sdept}', chinese = {chinese}, math = {math}, "
                    f"english = {english}, average_score = {average_score}, classmate_score = {classmate_score}, "
                    f"teacher_score = {teacher_score}, total_score = {total_score} WHERE sid = '{sid}'")
                sid_index = self.list_sid.index(sid)
                self.list_sname[sid_index] = sname
                self.list_sdept[sid_index] = sdept
                self.list_chinese[sid_index] = chinese
                self.list_math[sid_index] = math
                self.list_english[sid_index] = english
                self.list_average_score[sid_index] = average_score
                self.list_classmate_score[sid_index] = classmate_score
                self.list_teacher_score[sid_index] = teacher_score
                self.list_total_score[sid_index] = total_score
                self.tree.item(self.tree.get_children()[sid_index], values=(
                    sid, sname, sdept, chinese, math, english, average_score, classmate_score, teacher_score, total_score))
                messagebox.showinfo("showinfo", "修改学生成绩信息成功！")

    # 按学号查询某个学生成绩信息
    def select(self):
        if messagebox.askyesnocancel("askyesnocancel", "是否查询该学生成绩信息？"):
            sid = self.var_sid.get()
            if sid not in self.list_sid:
                messagebox.showwarning("showwarning", "该学生成绩信息不存在！")
            else:
                sid_index = self.list_sid.index(sid)
                self.var_sname.set(self.list_sname[sid_index])
                self.var_sdept.set(self.list_sdept[sid_index])
                self.var_chinese.set(self.list_chinese[sid_index])
                self.var_math.set(self.list_math[sid_index])
                self.var_english.set(self.list_english[sid_index])
                self.var_classmate_score.set(self.list_english[sid_index])
                self.var_teacher_score.set(self.list_teacher_score[sid_index])
                messagebox.showinfo("showinfo", "查询学生成绩信息成功！")

    # 删除学生成绩信息
    def delete(self):
        if messagebox.askyesnocancel("askyesnocancel", "是否删除该学生成绩信息？"):
            sid = self.var_sid.get()
            if sid not in self.list_sid:
                messagebox.showwarning("showwarning", "该学生成绩信息不存在！")
            else:
                utils = PyMySQLUtils()
                utils.execute(f"DELETE FROM student_score WHERE sid = '{sid}'")
                utils.close()
                sid_index = self.list_sid.index(sid)
                del self.list_sid[sid_index]
                del self.list_sname[sid_index]
                del self.list_sdept[sid_index]
                del self.list_chinese[sid_index]
                del self.list_math[sid_index]
                del self.list_english[sid_index]
                del self.list_average_score[sid_index]
                del self.list_classmate_score[sid_index]
                del self.list_teacher_score[sid_index]
                del self.list_total_score[sid_index]
                self.tree.delete(self.tree.get_children()[sid_index])
                messagebox.showinfo("showinfo", "删除学生成绩信息成功！")

    def back(self):
        if messagebox.askokcancel("askokcancel", "是否关闭该窗口？"):
            StartMenu(self.window)

class mysql_excel:
    def __init__(self, path):
        if messagebox.askyesnocancel("askyesnocancel", "是否写入到Excel文件？"):
            utils = PyMySQLUtils()
            results = utils.fetchall("SELECT * FROM student_score")
            book = xlwt.Workbook(encoding="utf-8")
            sheet = book.add_sheet("sheet1", cell_overwrite_ok=True)
            table_head = ["学号", "姓名", "院系", "语文成绩", "数学成绩", "英语成绩", "考试平均成绩", "同学互评分", "任课教师评分", "综合测评总分"]
            for i in range(len(table_head)):
                sheet.write(0, i, table_head[i])
            for row in range(len(results)):
                for col in range(len(results[row])):
                    print(results[row][col])
                    sheet.write(row+1, col, results[row][col])
            book.save(path)
            messagebox.showinfo("showinfo", "成功写入到Excel文件！")

class prepare:
    def create_table(self):
        utils = PyMySQLUtils()
        # 使用预处理语句创建表，若不存在则创建，若存在则跳过
        sql1 = """CREATE TABLE IF NOT EXISTS student_score(
                      sid varchar(32) PRIMARY KEY,
                      sname varchar(32) NOT NULL,
                      sdept varchar(32) NOT NULL,
                      chinese float(5,2) NOT NULL,
                      math float(5,2) NOT NULL,
                      english float(5,2) NOT NULL,
                      average_score float(5,2) NOT NULL,
                      classmate_score float(5,2) NOT NULL,
                      teacher_score float(5,2) NOT NULL,
                      total_score float(5,2) NOT NULL
                      ) ENGINE = InnoDB DEFAULT CHARSET = utf8
                   """
        utils.execute(sql1)
        # 使用预处理语句创建表，若不存在则创建，若存在则跳过
        sql2 = """CREATE TABLE IF NOT EXISTS teacher_login(
                      username varchar(32) NOT NULL,
                      password varchar(32) NOT NULL
                      ) ENGINE = InnoDB DEFAULT CHARSET = utf8
                   """
        utils.execute(sql2)
        utils.close()

    def excel_mysql(self):
        book = xlrd.open_workbook("E:\\PycharmProjects\\StudentScoreManagerSystem\\StudentScore.xlsx")
        sheet = book.sheet_by_index(0)
        utils = PyMySQLUtils()
        for i in range(1, sheet.nrows):
            sid = sheet.cell(i, 0).value
            sname = sheet.cell(i, 1).value
            sdept = sheet.cell(i, 2).value
            chinese = sheet.cell(i, 3).value
            math = sheet.cell(i, 4).value
            english = sheet.cell(i, 5).value
            average_score = sheet.cell(i, 6).value
            classmate_score = sheet.cell(i, 7).value
            teacher_score = sheet.cell(i, 8).value
            total_score = sheet.cell(i, 9).value
            utils.execute(
                f"INSERT INTO student_score VALUES('{sid}', '{sname}', '{sdept}', {chinese}, {math}, {english}, "
                f"{average_score}, {classmate_score}, {teacher_score}, {total_score})")
        utils.close()


if __name__ == '__main__':
    pre = prepare()
    pre.create_table()
    pre.excel_mysql()
    window = Tk()
    StartMenu(window)
