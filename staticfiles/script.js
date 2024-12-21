// Show Register Page
function showRegister() {
    document.getElementById("register-page").style.display = "block";
    document.getElementById("login-page").style.display = "none";
    document.getElementById("todo-page").style.display = "none";
}

// Show Login Page
function showLogin() {
    document.getElementById("register-page").style.display = "none";
    document.getElementById("login-page").style.display = "block";
    document.getElementById("todo-page").style.display = "none";
}

// Show To-Do Page
function showTodoPage(username) {
    document.getElementById("register-page").style.display = "none";
    document.getElementById("login-page").style.display = "none";
    document.getElementById("todo-page").style.display = "block";
    document.getElementById("username-display").innerText = username;
}

// Register Logic
document.getElementById("register-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const username = document.getElementById("reg-username").value;
    const password = document.getElementById("reg-password").value;

    if (localStorage.getItem(username)) {
        alert("Username already exists! Please login.");
    } else {
        localStorage.setItem(username, password);
        alert("Registration successful! Please login.");
        showLogin();
    }
});

// Login Logic
document.getElementById("login-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;

    const storedPassword = localStorage.getItem(username);
    if (storedPassword && storedPassword === password) {
        alert("Login successful!");
        showTodoPage(username);
    } else {
        alert("Invalid credentials! Try again.");
    }
});

// Logout Logic
function logout() {
    showLogin();
}

// To-Do List Logic
document.getElementById("add-task-btn").addEventListener("click", () => {
    const taskInput = document.getElementById("task-input");
    const task = taskInput.value.trim();

    if (task) {
        const taskList = document.getElementById("task-list");
        const li = document.createElement("li");

        li.innerHTML = `
            <span>${task}</span>
            <button onclick="this.parentElement.remove()">Delete</button>
        `;
        taskList.appendChild(li);
        taskInput.value = "";
    } else {
        alert("Please enter a task!");
    }
});
