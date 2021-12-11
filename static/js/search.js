var search = document.querySelector('.container input')
search.addEventListener('click', waitRequest)

function waitRequest() {
    this.className = 'active';
    var searchButton = this.nextElementSibling;

    this.addEventListener('keyup', function(e) {
        if (e.keyCode == 13) {
            window.location.href = `/tracks?q=${this.value}`;
        }
    })

    var self = this
    searchButton.addEventListener('click', function() {
        window.location.href = `/tracks?q=${self.value}`;
    })
}