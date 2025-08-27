import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Testlerden önce veri tabanını oluşturmak ve testlerden sonra temizlemek için kullanılan test düzeneği."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Test sırasında veri tabanı bağlantısı oluşturur ve testten sonra bağlantıyı kapatır."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Veri tabanı ve 'users' tablosunun oluşturulmasını test eder."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "'users' tablosu veri tabanında bulunmalıdır."

def test_add_new_user(setup_database, connection):
    """Yeni bir kullanıcının eklenmesini test eder."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Kullanıcı veri tabanına eklenmiş olmalıdır."


def test_add_existing_user(setup_database):
    result1 = add_user('duplicate', 'dup@example.com', 'secret123')
    result2 = add_user('duplicate', 'dup2@example.com', 'anotherpass')
    assert result1 is True
    assert result2 is False


def test_authenticate_success(setup_database):
    add_user('authuser', 'auth@example.com', 'mypassword')
    result = authenticate_user('authuser', 'mypassword')
    assert result is True


def test_authenticate_nonexistent_user(setup_database):
    result = authenticate_user('ghostuser', 'wrongpassword')
    assert result is False


def test_authenticate_wrong_password(setup_database):
    add_user('wrongpassuser', 'wp@example.com', 'correctpass')
    result = authenticate_user('wrongpassuser', 'wrongpass')
    assert result is False


def test_display_users(setup_database, capsys):
    add_user('listuser1', 'list1@example.com', 'pass1')
    add_user('listuser2', 'list2@example.com', 'pass2')

    display_users()
    captured = capsys.readouterr()

    assert 'listuser1' in captured.out
    assert 'listuser2' in captured.out




# İşte yazabileceğiniz bazı testler:
"""
Var olan bir kullanıcı adıyla kullanıcı eklemeye çalışmayı test etme.
Başarılı kullanıcı doğrulamasını test etme.
Var olmayan bir kullanıcıyla doğrulama yapmayı test etme.
Yanlış şifreyle doğrulama yapmayı test etme.
Kullanıcı listesinin doğru şekilde görüntülenmesini test etme.
"""
