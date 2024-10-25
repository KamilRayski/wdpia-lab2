function generateId() {
    return 'xxxx-xxxx-xxxx-xxxx'.replace(/[x]/g, function () {
        return (Math.random() * 16 | 0).toString(16);
    });
}

async function loadUserList() {
    try {
        const response = await fetch('http://localhost:8000');
        if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }
        const users = await response.json();
        displayUsers(users);
    } catch (error) {
        console.error('Error loading users:', error);
        alert("Failed to load users: " + error.message);
    }
}

async function addUser() {
    const firstName = document.getElementById('first-name').value;
    const lastName = document.getElementById('last-name').value;
    const role = document.getElementById('role').value;
    const id=generateId();

    if (!firstName || !lastName || !role) {
        alert("Please fill out all fields.");
        return;
    }

    const newUser = { first_name: firstName, last_name: lastName, role: role, user_id: id };

    try {
        const response = await fetch('http://localhost:8000', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(newUser)
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }

        //alert("User added successfully!");
        document.getElementById('first-name').value = '';
        document.getElementById('last-name').value = '';
        document.getElementById('role').value = '';

        await loadUserList();

    } catch (error) {
        console.error('Error adding user:', error);
    }
}

async function deleteUser(userId) {
    try {
        const response = await fetch(`http://localhost:8000/${userId}`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) {
            const errorResponse = await response.json();
            throw new Error(errorResponse.error || `Error: ${response.status}`);
        }

        const successMessage = await response.json();

        await loadUserList();

    } catch (error) {
        console.error('Error deleting user:', error);
        alert("Failed to delete user: " + error.message);
    }
}

function displayUsers(users) {
    const userList = document.querySelector('.user-list');
    userList.innerHTML = '';

    if (users.length === 0) {
        userList.innerHTML = '<p>No users found.</p>';
    } else {
        users.forEach(user => {
            const userItem = document.createElement('div');
            userItem.classList.add('user-item');
            userItem.innerHTML = `
                <p><strong>${user.first_name} ${user.last_name}</strong></p>
                <span>${user.role}</span>
                <button class="delete-btn" onclick="deleteUser('${user.user_id}')"><img src="recycle-bin.png"></button>
            `;
            userList.appendChild(userItem);
        });
    }
}

window.addEventListener('load', function () {
    loadUserList();
});
