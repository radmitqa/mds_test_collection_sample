import subprocess

def run_tests(test_scenarios=None):
    """
    Run specific test scenarios.
    :param test_scenarios: List of test scenario paths to run. If None, runs all tests.
    """
    if test_scenarios:
        for scenario in test_scenarios:
            print(f"Running test scenario: {scenario}")
            subprocess.run(["pytest", scenario])
    else:
        print("Running all tests...")
        subprocess.run(["pytest"])


if __name__ == "__main__":
    print("Test Collection Manager")
    print("1. Run All Tests")
    print("2. Run Specific Scenarios")
    choice = input("Choose an option (1 or 2): ").strip()

    if choice == "1":
        run_tests()
    elif choice == "2":
        print("Available Test Scenarios:")
        test_files = [
            "tests/test_case_1.py",
            "tests/test_case_2.py",
            "tests/test_case_3.py",
            "tests/test_case_4.py",
            "tests/test_case_5.py",
        ]
        for i, file in enumerate(test_files, start=1):
            print(f"{i}. {file}")
        selected = input("Enter the numbers of the scenarios to run (comma-separated): ").strip()
        try:
            selected_indices = [int(x) - 1 for x in selected.split(",")]
            selected_tests = [test_files[i] for i in selected_indices if 0 <= i < len(test_files)]
            if selected_tests:
                run_tests(selected_tests)
            else:
                print("No valid scenarios selected.")
        except ValueError:
            print("Invalid input. Please enter numbers only.")
    else:
        print("Invalid choice. Exiting.")
