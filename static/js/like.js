document.querySelector('.heart').addEventListener('click', function() {
    this.classList.toggle('is_animating')

    trackId = this.getAttribute('data-id')
    window.location.href = `/recs?id=${trackId}`
})