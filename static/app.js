let fadeElement = [...document.querySelectorAll('.fade-up')]

let options = {
    rootMargin: '-10%',
    threshold: 0.0
}

let observer = new IntersectionObserver(showItem, options);

function showItem(entries){
    entries.forEach(entry => {
        if(entry.isIntersecting){
            entry.target.classList.add('active');
        }
    })
}

fadeElement.forEach(item => {
    observer.observe(item);
})