function changeVideo(videoId) {
    const iframe = document.getElementById('main-video');
    iframe.src = `https://www.youtube.com/embed/${videoId}`;
}
