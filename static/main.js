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
            body: Time to take ${medicine},
            icon: "/static/img/medicine.png"
        });
    } else {
        alert("Time to take " + medicine);
    }
}

// Check every minute
function checkMedicineTime() {
    let now = new Date();
    let current = now.getHours().toString().padStart(2, '0') + ":" +
                  now.getMinutes().toString().padStart(2, '0');

    fetch("/get_medicines")
        .then(res => res.json())
        .then(meds => {
            meds.forEach(med => {
                if (med.time === current) {
                    showReminder(med.name);
                }
            });
        });
}

setInterval(checkMedicineTime, 60000);