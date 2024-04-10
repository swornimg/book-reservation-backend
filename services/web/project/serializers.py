from flask import jsonify, make_response


class UserRegistrationSerializer:
    def __init__(self, data):
        self.data = data

    def validate(self):
        errors = {}
        required_fields = ['email', 'first_name', 'last_name', 'password']
        
        for field in required_fields:
            if field not in self.data:
                errors[field] = f"{field.capitalize()} is required!"
        
        return errors

    def response(self):
        errors = self.validate()
        if errors:
            return False, errors
        return True, self.data