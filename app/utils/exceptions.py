from fastapi import status, HTTPException


def get_user_exception() -> HTTPException:
    """ Returns exception for unauthorized access. """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return credentials_exception


def token_exception() -> HTTPException:
    """ Returns exception for invalid username or password. """
    
    token_exception_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return token_exception_response


def todo_not_found_exception(id: int) -> HTTPException:
    """ Returns exception for todo not exist. """

    todo_not_found_exception_response = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Todo with {id} not found."
    )
    return todo_not_found_exception_response


def user_not_exist_exception() -> HTTPException:
    """ Returns exception for user not exist. """

    user_not_exist_exception_response = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User doesnot exist"
        )
    return user_not_exist_exception_response