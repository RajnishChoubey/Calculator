import streamlit as st

st.title("Simple Calculator App")

num1 = st.number_input("Enter first number", format="%f")
num2 = st.number_input("Enter second number", format="%f")

operation = st.selectbox("Select operation", ["Add", "Subtract", "Multiply", "Divide"])

if st.button("Calculate"):
    if operation == "Add":
        result = num1 + num2
    elif operation == "Subtract":
        result = num1 - num2
    elif operation == "Multiply":
        result = num1 * num2
    elif operation == "Divide":
        if num2 == 0:
            result = "Error: Division by zero"
        else:
            result = num1 / num2
    st.success(f"Result: {result}")
