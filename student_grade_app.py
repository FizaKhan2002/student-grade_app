import streamlit as st
import pandas as pd

# Initialize session state
if "student_data" not in st.session_state:
    st.session_state.student_data = {}

st.title("🎓 Student Grade Management System")

st.sidebar.header("Actions")
action = st.sidebar.selectbox("Select Action", ["Add", "Update", "Delete", "Show All", "Analyze"])

# Helper function to calculate grade
def get_grade(avg):
    if avg >= 90:
        return "A+"
    elif avg >= 80:
        return "A"
    elif avg >= 70:
        return "B"
    elif avg >= 60:
        return "C"
    elif avg >= 50:
        return "D"
    else:
        return "F"

# Add student
if action == "Add":
    st.header("➕ Add Student Record")
    name = st.text_input("Student Name")
    grades = st.text_input("Grades (comma-separated, e.g., 85,90,78)")

    if st.button("Add"):
        if name and grades:
            try:
                grade_list = [int(i.strip()) for i in grades.split(',')]
                st.session_state.student_data[name] = grade_list
                st.success(f"Added {name}'s record.")
            except ValueError:
                st.error("Please enter numeric grades only.")
        else:
            st.warning("Please enter both name and grades.")

# Update student
elif action == "Update":
    st.header("✏️ Update Student Record")
    name = st.text_input("Existing Student Name")
    new_grades = st.text_input("New Grades (comma-separated)")

    if st.button("Update"):
        if name in st.session_state.student_data:
            try:
                grade_list = [int(i.strip()) for i in new_grades.split(',')]
                st.session_state.student_data[name] = grade_list
                st.success(f"Updated {name}'s record.")
            except ValueError:
                st.error("Please enter numeric grades only.")
        else:
            st.error(f"No record found for {name}")

# Delete student
elif action == "Delete":
    st.header("🗑️ Delete Student Record")
    name = st.text_input("Student Name to Delete")

    if st.button("Delete"):
        if name in st.session_state.student_data:
            del st.session_state.student_data[name]
            st.success(f"Deleted record for {name}")
        else:
            st.error(f"No record found for {name}")

# Show all student data
elif action == "Show All":
    st.header("📋 All Student Records")
    if st.session_state.student_data:
        for student, grades in st.session_state.student_data.items():
            st.write(f"**{student}**: {grades}")
    else:
        st.info("No student records found.")



# Analyze student data
elif action == "Analyze":
    st.header("📊 Student Performance Analyzer")

    if st.session_state.student_data:
        # Build DataFrame
        df = pd.DataFrame([
            {
                "Name": name,
                "Average": sum(grades) / len(grades)
            }
            for name, grades in st.session_state.student_data.items()
        ])

        df = df.sort_values(by="Average", ascending=False).reset_index(drop=True)

        st.subheader("📈 Average Marks per Student")
        st.bar_chart(df.set_index("Name"))

        st.subheader("🏅 Top Performer")
        top = df.iloc[0]
        st.success(f"{top['Name']} with average marks {top['Average']:.2f}")

        st.subheader("📋 Raw Data")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No student records to analyze.")


        st.subheader("📊 Total Marks Comparison")
        st.bar_chart(data=df, x="Name", y="Total")

        st.subheader("🏅 Top Performer")
        st.success(f"{df.iloc[0]['Name']} with {df.iloc[0]['Total']} marks!")

    else:
        st.info("No student records to analyze.")
