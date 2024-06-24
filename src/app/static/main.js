const toggleViewBtn = document.getElementById('toggle-view');
const movieList = document.querySelector('.movie-list');

let isGridView = false;

try {
    toggleViewBtn.addEventListener('click', () => {
        if (!isGridView) {
            movieList.classList.add('grid-view');
            toggleViewBtn.innerHTML = '<i class="fa fa-list"></i>';
            setViewType(true);
        } else {
            movieList.classList.remove('grid-view');
            toggleViewBtn.innerHTML = '<i class="fa fa-th-large"></i>';
            setViewType(false);
        }
        isGridView = !isGridView;
    });
} catch (e) {
    console.log('toggleViewBtn is null, no event listener added.');
}

function setViewType(isGridView) {
    localStorage.setItem('viewType', isGridView ? 'grid' : 'list');
}

function getViewType() {
    return localStorage.getItem('viewType');
}

document.addEventListener('DOMContentLoaded', function() {
    const viewType = getViewType();
    const movieList = document.querySelector('.movie-list');

    if (viewType === 'grid') {
        movieList.classList.add('grid-view');
        toggleViewBtn.innerHTML = '<i class="fa fa-list"></i>';
        isGridView = true;
    }
});

function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
  });
}

window.addEventListener('scroll', function() {
    var toTopBtn = document.getElementById('toTop');
    if (window.pageYOffset > 600) {
        toTopBtn.style.display = 'block';
    } else {
        toTopBtn.style.display = 'none';
    }
});
