// Client-side form validation (additional to server-side)
document.querySelector('form')?.addEventListener('submit', function(e) {
    const name = document.querySelector('#name');
    const email = document.querySelector('#email');
    const subject = document.querySelector('#subject');
    const message = document.querySelector('#message');
    
    if (!name.value || !email.value || !subject.value || !message.value) {
        e.preventDefault();
        alert('All fields are required!');
    } else if (!/\S+@\S+\.\S+/.test(email.value)) {
        e.preventDefault();
        alert('Invalid email format!');
    }
});

// Animated counters on About page
const counters = document.querySelectorAll('.counter');
const speed = 200; // Adjust speed

counters.forEach(counter => {
    const updateCount = () => {
        const target = +counter.getAttribute('data-target');
        const count = +counter.innerText;
        const inc = target / speed;

        if (count < target) {
            counter.innerText = Math.ceil(count + inc);
            setTimeout(updateCount, 1);
        } else {
            counter.innerText = target;
        }
    };
    updateCount();
});