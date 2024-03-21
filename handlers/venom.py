import yaml
import json
import copy

def write_tests(cases: list[dict] = None):
    """
    Generate Venom test cases from a list of input cases and write them to a YAML file.

    Params:
    - cases (list[dict]): List of input cases containing information for test generation. Each case should be a dictionary with specific keys.
    """

    def generate_expect_conditions(json_data):
        """
        Recursively generate expect conditions for assertions from a JSON data structure.

        Params:
        - json_data: JSON data structure to generate expect conditions from.

        Returns:
        - List of expect conditions.
        """

        expect_conditions = []

        for key, value in json_data.items():
            if value is None:
                expect_conditions.append({key: "null"})
            elif isinstance(value, dict):
                # Recursively generate expect conditions for nested dictionaries
                nested_conditions = generate_expect_conditions(value)
                expect_conditions.append({key: nested_conditions})
            else:
                expect_conditions.append({key: value})

        return expect_conditions

    def parse_case_to_venom_test(case: dict, template: dict) -> dict:
        """
        Parse a single input case into a Venom test case using a given template.

        Params:
        - case (dict): Input case to be parsed.
        - template (dict): Template for the Venom test.

        Returns:
        - Parsed Venom test case.
        """

        test = copy.deepcopy(template)

        # Check name
        if "name" in case and case["name"] is not None:
            test["name"] = case["name"]

        # Check type
        if "type" in case and case["type"] is not None:
            test["steps"][0]["type"] = case["type"]

        # Check method
        if "method" in case and case["method"] is not None:
            test["steps"][0]["method"] = case["method"]

        # Check url
        if "url" in case and case["url"] is not None:
            test["steps"][0]["url"] = case["url"]

        # Check assertions
        if "assertions" in case and case["assertions"] is not None:
            test["steps"][0]["assertions"] = case["assertions"]

        # Check expectations
        expectations = generate_expect_conditions(case["json_response"])

        if len(expectations) > 0:
            test["steps"][0]["expect"] = expectations
        else:
            test["steps"][0].pop("expect")

        # Check body
        if len(case["json_request"].keys()) > 0:
            test["steps"][0]["body"] = f'{json.dumps(case["json_request"])}'
        else:
            test["steps"][0].pop("body")

        return test

    # Check if cases is empty
    if cases is None:
        print("[ERROR] No cases were specified")
        return

    template = {
        "name": "Name",
        "testcases": []
    }
    
    test_template = {
        "name": "",
        "steps": [
            {
                "type": "",
                "method": "",
                "url": "",
                "body": "",
                "assertions": [],
                "expect": []
            }
        ]
    }

    generated_tests = []

    # Generate the test
    for case in cases:
        generated_tests.append(parse_case_to_venom_test(case, test_template))

    template["testcases"] = generated_tests

    # Export the tests
    with open('tests.yaml', 'w') as file:
        yaml.dump(template, file)
