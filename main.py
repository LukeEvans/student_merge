import pandas as pd

STUDENTS = 'input/application.csv'
TEACHERS = 'input/teacher.csv'
COUNSELORS = 'input/counselor.csv'
PARENTS = 'input/parent.csv'

students_df = pd.read_csv(STUDENTS)
student_data = students_df.drop(columns=["Timestamp", "Teacher's name you asked for a recommendation ",
                                         "Counselor's name you asked for a recommendation "])

teacher_df = pd.read_csv(TEACHERS)
teacher_data = teacher_df.drop(columns=["Timestamp", "Student First Name", "Student Last Name", "School"])

counselor_df = pd.read_csv(COUNSELORS)
counselor_data = counselor_df.drop(
    columns=["Timestamp", "Student First Name", "Student Last Name", "School"])

parent_df = pd.read_csv(PARENTS)
parent_data = parent_df.drop(
    columns=["Timestamp", "Your student's ID number", "Your student's first name", "Your student's last name",
             "Email Address"])


def get_teacher_counselor_data(student_first, student_last, data_frame, data):
    student_first = str(student_first)
    student_last = str(student_last)
    found_index = -1
    for index, row in data_frame.iterrows():
        first = str(row["Student First Name"])
        last = str(row["Student Last Name"])

        if first.lower() == student_first.lower() and last.lower() == student_last.lower():
            found_index = index
            break

    if found_index > -1:
        return data.iloc[found_index]
    else:
        first_two = student_first[0:2]
        for index, row in data_frame.iterrows():
            first = str(row["Student First Name"])[0:2]
            last = str(row["Student Last Name"])

            if first.lower() == first_two.lower() and last.lower() == student_last.lower():
                found_index = index
                break

        if found_index > -1:
            return data.iloc[found_index]

    return None


def get_parent_data(student_id):
    found_index = -1
    for index, row in parent_df.iterrows():
        if row["Your student's ID number"] == student_id:
            found_index = index
            break

    if found_index > -1:
        return parent_data.iloc[found_index]

    return None


def write_line(output_file, original_line):
    new_line = []
    for i in original_line:
        new_line.append(i.replace("\n", "").replace(",", ""))
    output_file.write(','.join(new_line))
    output_file.write("\n")


if __name__ == '__main__':
    results = []
    for _, student_row in student_data.iterrows():
        first = student_row["First Name"]
        last = student_row["Last Name"]
        id_number = student_row["Student ID Number"]

        teacher_row = get_teacher_counselor_data(first, last, teacher_df, teacher_data)
        counselor_row = get_teacher_counselor_data(first, last, counselor_df, counselor_data)
        parent_row = get_parent_data(id_number)

        result = pd.concat([student_row, teacher_row, counselor_row, parent_row])
        results.append(result)

    results_df = pd.DataFrame(results)
    results_df.to_csv("output.csv", index=False)
