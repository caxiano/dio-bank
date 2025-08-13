from http import HTTPStatus
from unittest.mock import Mock

import pytest

from src.utils import requires_roles, squareroot


@pytest.mark.parametrize('test_input,expected', [(2, 4), (3, 9), (5, 25)])
def test_squareroot(test_input, expected):
    result = squareroot(test_input)
    assert result == expected


@pytest.mark.parametrize(
    'test_input,exc_class,msg',
    [
        ('a', TypeError, "unsupported operand type(s) for ** or pow(): 'str' and 'int'"),
        (None, TypeError, "unsupported operand type(s) for ** or pow(): 'NoneType' and 'int'")
    ]
)
def test_squareroot_negative(test_input, exc_class, msg):
    with pytest.raises(exc_class) as exc:
        squareroot(test_input)
        assert str(
            exc.value) == msg


def test_requires_roles_success(mocker):
    # Given
    mock_user = mocker.Mock()
    mock_user.role.name = 'admin'

    mocker.patch('src.utils.get_jwt_identity')
    mocker.patch('src.utils.db.get_or_404', return_value=mock_user)
    decorated_function = requires_roles('admin')(lambda: 'success')

    # When
    result = decorated_function()

    # Then
    assert result == 'success'


def test_requires_roles_fail(mocker):
    # Given
    mock_user = mocker.Mock()
    mock_user.role.name = 'guest'

    mocker.patch('src.utils.get_jwt_identity')
    mocker.patch('src.utils.db.get_or_404', return_value=mock_user)
    decorated_function = requires_roles('admin')(lambda: 'success')

    # When
    result = decorated_function()

    # Then
    assert result == ({'message': 'User dont have access'},
                      HTTPStatus.FORBIDDEN)
