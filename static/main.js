// Ask for Notification Permission
function enableNotifications() {
    Notification.requestPermission().then(result => {
        alert("Notifications: " + result);
    });
}

// Show notification
function showReminder(medicine) {
    if (Notification.permission === "granted") {
        new Notification("DoseBuddy Reminder", {
            body: `Time to take ${medicine}`,
            icon: "/static/img/medicine.png"
        });
    } else {
        alert("Time to take " + medicine);
    }
}

// Check every minute
function checkMedicineTime() {
    let now = new Date();
    let current =
        now.getHours().toString().padStart(2, '0') + ":" +
        now.getMinutes().toString().padStart(2, '0');

    fetch("/get_medicines")
        .then(res => res.json())
        .then(meds => {
            meds.forEach(med => {
                if (med.time === current) {
                    showReminder(med.name);
                }
            });
        })
        .catch(err => console.error("Error fetching medicines:", err));
}
// theme toggle
const toggle = document.getElementById("themeToggle");
toggle.addEventListener("click", () => {
    document.body.classList.toggle("light");
    localStorage.setItem("theme", document.body.classList.contains("light") ? "light" : "dark");
});

// load saved theme
if (localStorage.getItem("theme") === "light") {
    document.body.classList.add("light");
}

// notifications
document.getElementById("notifyBtn").addEventListener("click", async () => {
    if (!("Notification" in window)) {
        alert("Notifications not supported");
        return;
    }

    const permission = await Notification.requestPermission();
    alert("Notification permission: " + permission);
});

// Runs every minute
setInterval(checkMedicineTime, 60000);





