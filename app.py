from appconfig import AppConfig
from azureai import AzureAI
import streamlit as st
config = AppConfig()
azure_ai = AzureAI(config)
llm=azure_ai.get_client()

class LanguageValidator:
    """
    Validates if the programming language provided by the user matches the actual language of the code.
    """
    def __init__(self, openai_engine):
        self.openai_engine = openai_engine

    def detect_language(self, code):
        """
        Uses OpenAI to detect the programming language of the given code.
        """
        prompt = (
            "Analyze the following code and identify its programming language:\n\n"
            f"{code}\n\n"
            "Provide only the name of the programming language in your response."
        )
        try:
            response = llm.invoke(prompt)

            detected_language = response.content.strip().lower()
            return detected_language
        except Exception as e:
            raise Exception(f"Error during language detection: {e}")

    def validate_language(self, expected_language, code):
        """
        Compares the detected programming language with the expected one.
        """
        detected_language = self.detect_language(code)
        if detected_language != expected_language.lower():
            raise ValueError(
                f"The input programming language '{expected_language}' does not match the detected language '{detected_language}'."
            )
        return detected_language


class TestCaseGenerator:
    """
    Generates test cases for the given code in the specified programming language.
    """
    def __init__(self, openai_engine):
        self.openai_engine = openai_engine

    def generate_test_cases(self, language, code):
        """
        Uses OpenAI to generate test cases for the given code.
        """
        prompt = (
            f"Generate detailed test cases for the following {language} code:\n\n"
            f"{code}\n\n"
            "Provide the test cases in a clear and concise format."
        )
        try:
            response = llm.invoke(prompt)
            return response.content.strip()
        except Exception as e:
            raise Exception(f"Error during test case generation: {e}")

#Uncomment this code for pythin input test
# class TestCaseApp:
#     """
#     Manages the interaction between the user and the application.
#     """
#     def __init__(self, language_validator, test_case_generator):
#         self.language_validator = language_validator
#         self.test_case_generator = test_case_generator

#     def run(self):
#         """
#         Main loop of the application.
#         """
#         print("Welcome to the Test Case Generator!")
#         print("Provide the details below to generate test cases for your code.\n")

#         # Collect inputs from the user
#         programming_language = input("Enter the programming language (e.g., Python, JavaScript): ").strip()
#         if not programming_language:
#             print("Programming language cannot be empty.")
#             return

#         print("\nEnter the code for which you want test cases (press Enter twice to finish):")
#         code_lines = []
#         while True:
#             line = input()
#             if line == "":
#                 break
#             code_lines.append(line)
#         code_input = "\n".join(code_lines)

#         if not code_input:
#             print("Code cannot be empty.")
#             return

#         # Validate programming language
#         try:
#             print("\nValidating programming language...")
#             detected_language = self.language_validator.validate_language(programming_language, code_input)
#             print(f"Detected programming language: {detected_language.capitalize()}")
#         except ValueError as ve:
#             print(f"Error: {ve}")
#             return
#         except Exception as e:
#             print(f"Unexpected error during validation: {e}")
#             return

#         # Generate test cases
#         try:
#             print("\nGenerating test cases...")
#             test_cases = self.test_case_generator.generate_test_cases(programming_language, code_input)
#             print("\nGenerated Test Cases:")
#             print("-" * 30)
#             print(test_cases)
#         except Exception as e:
#             print(f"Error during test case generation: {e}")


# if __name__ == "__main__":
#     # Create instances of the classes
#     language_validator = LanguageValidator(openai_engine="YOUR_DEPLOYMENT_NAME")
#     test_case_generator = TestCaseGenerator(openai_engine="YOUR_DEPLOYMENT_NAME")

#     # Run the application
#     app = TestCaseApp(language_validator, test_case_generator)
#     app.run()

#Streamlit
class TestCaseApp:
    """
    Manages the interaction between the user and the application via Streamlit.
    """
    def __init__(self, language_validator, test_case_generator):
        self.language_validator = language_validator
        self.test_case_generator = test_case_generator

    def run(self):
        """
        Renders the Streamlit UI and handles user interaction.
        """
        st.title("Test Case Generator")
        st.write("Provide the details below to generate test cases for your code.")

        # Collect inputs from the user
        programming_language = st.text_input("Programming Language (e.g., Python, JavaScript)").strip()
        code_input = st.text_area("Code (paste your code here)")

        if st.button("Generate Test Cases"):
            if not programming_language:
                st.error("Programming language cannot be empty.")
                return
            if not code_input:
                st.error("Code cannot be empty.")
                return

            # Validate programming language
            try:
                with st.spinner("Validating programming language..."):
                    detected_language = self.language_validator.validate_language(programming_language, code_input)
                st.success(f"Detected programming language: {detected_language.capitalize()}")
            except ValueError as ve:
                st.error(f"Error: {ve}")
                return
            except Exception as e:
                st.error(f"Unexpected error during validation: {e}")
                return

            # Generate test cases
            try:
                with st.spinner("Generating test cases..."):
                    test_cases = self.test_case_generator.generate_test_cases(programming_language, code_input)
                st.subheader("Generated Test Cases")
                st.code(test_cases, language=programming_language)
            except Exception as e:
                st.error(f"Error during test case generation: {e}")


if __name__ == "__main__":
    # Create instances of the classes
    language_validator = LanguageValidator(openai_engine="YOUR_DEPLOYMENT_NAME")
    test_case_generator = TestCaseGenerator(openai_engine="YOUR_DEPLOYMENT_NAME")

    # Run the application
    app = TestCaseApp(language_validator, test_case_generator)
    app.run()
