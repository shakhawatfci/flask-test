def validate_input(name, password , email):
    errors = []

    # Validate name
    if not name:
        errors.append('Username is required.')
        
    if not email:
        errors.append('email is required.')

    # Validate password
    if not password:
        errors.append('Password is required.')
    elif len(password) < 6:
        errors.append('Password must be at least 6 characters long.')

    return errors


def validate_user_update_input(name , email):
    errors = []

    # Validate name
    if not name:
        errors.append('Username is required.')
        
    if not email:
        errors.append('email is required.')

    return errors