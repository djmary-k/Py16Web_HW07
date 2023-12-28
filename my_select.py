from sqlalchemy import func, desc, select, and_
from conf.models import Grade, Teacher, Student, Group, Subject
from conf.db import session


# Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_01():
    """
    SELECT
        s.id,
        s.fullname,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM students s
    JOIN grades g ON s.id = g.student_id
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 5;
    """
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Student).join(Grade).group_by(Student.id).order_by(desc('average_grade')).limit(5).all()
    return result

# Знайти студента із найвищим середнім балом з певного предмета.
def select_02():
    """
    SELECT
        s.id,
        s.fullname,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM grades g
    JOIN students s ON s.id = g.student_id
    where g.subject_id = 1
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 1;
    """
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Student).filter(Grade.subjects_id == 1).group_by(Student.id).order_by(
        desc('average_grade')).limit(1).all()
    return result


# Знайти середній бал у групах з певного предмета.
def select_03():
    """
    SELECT
        groups.name,
        AVG(grades.grade) as average_grade
    from groups
    JOIN students s ON groups.id = students.group_id
    JOIN grades g ON students.id = g.student_id
    where g.subject_id = 1
    GROUP BY groups.name;
    """

    result = session.query(Group.name, func.round(func.avg(Grade.grade), 2).label("average_grade")) \
        .select_from(Group).join(Student).join(Grade).filter(Grade.subjects_id == 1).group_by(Group.name).all()
    return result

# Знайти середній бал на потоці (по всій таблиці оцінок).
def select_04():
    """
    SELECT
        ROUND(AVG(g.grade), 2) AS average_grade
        FROM grades g;
    """

    result = session.query(func.round(func.avg(Grade.grade), 2).label("average_grade")).select_from(Grade).all()
    return result

# Знайти які курси читає певний викладач.
def select_05():
    """
    SELECT
        t.full_name,
        s.name AS subject_name
    FROM teachers t
    JOIN subjects s ON t.id = s.teacher_id
    WHERE t.id = 1;
        """

    result = session.query(Teacher.fullname, Subject.name.label("subject_name")).select_from(Teacher).join(
        Subject).filter(Teacher.id == 1).all()
    return result

# Знайти список студентів у певній групі.
def select_06():
    """
    SELECT
        s.id,
        s.full_name
    FROM students s
    JOIN groups g ON s.group_id = g.id
    WHERE g.id = 1;
    """

    result = session.query(Student.id, Student.fullname).select_from(Student).join(Group).filter(Group.id == 1).all()
    return result

# Знайти оцінки студентів у окремій групі з певного предмета.
def select_07():
    """
    SELECT
        s.full_name,
        g.grade,
        subj.name AS subject_name
    FROM students s
    JOIN grades g ON s.id = g.student_id
    JOIN subjects subj ON g.subject_id = subj.id
    WHERE s.group_id = 2 AND subj.id = 1;
    """

    result = session.query(Student.fullname, Grade.grade, Subject.name.label("subject_name")) \
        .select_from(Student).join(Grade).join(Subject).filter(Student.group_id == 2).filter(Subject.id == 1).all()
    return result

# Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_08():
    """
    SELECT
        t.full_name,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM grades g
    JOIN subjects s ON g.subject_id = s.id
    JOIN teachers t ON s.teacher_id = t.id
    WHERE t.id = 2
    GROUP BY t.full_name;
    """

    result = session.query(Teacher.fullname, func.round(func.avg(Grade.grade), 2).label("average_grade")).select_from(
        Grade).join(Subject).join(Teacher).filter(Teacher.id == 2).group_by(Teacher.fullname).all()
    return result

# Знайти список курсів, які відвідує певний студент.
def select_09():
    """
    SELECT
        s.full_name,
        subj.name AS subject_name
    FROM students s
    JOIN grades g ON g.student_id = s.id
    JOIN subjects subj ON g.subject_id = subj.id
    WHERE s.id = 3;
    """

    result = session.query(Student.fullname,
                           Subject.name.label("subject_name")).select_from(Student).join(Grade).join(Subject).filter(
        Student.id == 3).all()
    return result

# Список курсів, які певному студенту читає певний викладач.
def select_10():
    """
    SELECT
        s.full_name,
        subj.name AS subject_name,
        t.full_name
    FROM students s
    JOIN grades g ON s.id = g.student_id
    JOIN subjects subj ON g.subject_id = subj.id
    JOIN teachers t ON subj.teacher_id = t.id
    WHERE s.id = 3 AND t.id = 2;
    """

    result = session.query(Student.fullname, Subject.name.label("subject_name"), Teacher.fullname).select_from(Student) \
        .join(Grade).join(Subject).join(Teacher).filter(Student.id == 3).filter(Teacher.id == 2).all()
    return result



if __name__ == "__main__":
    print(select_01())
    print(select_02())
    print(select_03())
    print(select_04())
    print(select_05())
    print(select_06())
    print(select_07())
    print(select_08())
    print(select_09())
    print(select_10())
