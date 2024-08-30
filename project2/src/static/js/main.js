


function confirmDelete(){
    const ok = confirm("Are You Sure? ") //a pop up
    if(!ok){
        event.preventDefault()
    }
}

const errorSpan = document.querySelector('.error');
if(errorSpan){
    setTimeout(()=>{
        errorSpan.parentNode.removeChild(errorSpan)
    },4000); 
}

// Purpose: To save user data (such as an email) on the client side, which can be used later without requiring the user to re-enter it.
function saveUser(){
    let email = document.getElementById("email").value;
    localStorage.setItem("email", email);
    alert("User saved: " + email);
}


function loginFirst(){
    alert("Please Login First")
}


//likes
document.addEventListener('DOMContentLoaded', () => {
    const likeIcon = document.getElementById('like-icon');
    const likeCountSpan = document.getElementById('like-count');

    let isLiked = likeIcon.getAttribute('data-user-has-liked') === 'True';

    // Set initial color based on like status
    const svgElement = likeIcon.querySelector('svg');
    updateHeartColor(svgElement, isLiked);

    likeIcon.addEventListener('click', () => {
        const vacationId = likeIcon.getAttribute('data-vacation-id');
        const action = isLiked ? 'unlike' : 'like';

        fetch(`/vacation/${vacationId}/${action}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                isLiked = !isLiked;  // Toggle the like status

                // Update the heart color based on the new status
                updateHeartColor(svgElement, isLiked);

                // Update the like count display
                likeCountSpan.textContent = data.like_count;
            } else {
                console.error('Failed to update like status:', data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});

function updateHeartColor(svgElement, isLiked) {
    if (isLiked) {
        svgElement.setAttribute('fill', 'red');
        svgElement.setAttribute('stroke', 'none');
    } else {
        svgElement.setAttribute('fill', 'none');
        svgElement.setAttribute('stroke', 'gray');
    }
}




//home profile page
document.addEventListener('scroll', function() {
    const elements = document.querySelectorAll('.profile-body, .profile-actions');
    elements.forEach(el => {
        const rect = el.getBoundingClientRect();
        if (rect.top < window.innerHeight) {
            el.classList.add('visible');
        }
    });
});


//header footer 
