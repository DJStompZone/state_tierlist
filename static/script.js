const states = document.querySelectorAll('#minimap path');
const tiers = document.querySelectorAll('.tier');

let selectedState = null;


function updateMinimap(stateId, tier) {
    const minimapState = document.querySelector(`#minimap path[id="${stateId}"]`);
    const color = getTierColor(tier);
    if (minimapState) {
        minimapState.style.fill = color;
    }
}

function getTierColor(tier) {
    const tierColors = {
        'S': '#FFD700',
        'A': '#C0C0C0',
        'B': '#CD7F32',
        'C': '#00FF00',
        'D': '#FFA500',
        'F': '#FF0000'
    };
    return tierColors[tier] || '#f9f9f9';
}

document.addEventListener('DOMContentLoaded', () => {


    // Add dragstart event to states
    states.forEach(state => {
        state.addEventListener('dragstart', event => {
            event.dataTransfer.setData('text/plain', state.id);
        });
    });

    // Allow tiers to accept drops
    tiers.forEach(tier => {
        tier.addEventListener('dragover', event => {
            event.preventDefault();
            tier.style.backgroundColor = '#e0e0e0'; // Highlight on dragover
        });

        tier.addEventListener('dragleave', () => {
            tier.style.backgroundColor = '#f9f9f9'; // Reset background
        });

        tier.addEventListener('drop', event => {
            event.preventDefault();
            const stateId = event.dataTransfer.getData('text/plain');
            const stateElement = document.getElementById(stateId);
            stateElement.setAttribute('data-tier', tier.getAttribute('data-tier'));
            tier.appendChild(stateElement);
            tier.style.backgroundColor = '#f9f9f9';
            updateMinimap(stateId, tier.getAttribute('data-tier'));
        });
    });


    // State selection
    states.forEach(state => {
        state.addEventListener('click', () => {
            if (selectedState) {
                selectedState.classList.remove('selected');
            }
            selectedState = state;
            state.classList.add('selected');
        });
    });

    // Tier placement
    tiers.forEach(tier => {
        tier.addEventListener('click', () => {
            if (selectedState) {
                let blankSvg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
                blankSvg.setAttribute('width', '100%');
                blankSvg.setAttribute('height', '100%');
                blankSvg.setAttribute('viewBox', '0 0 30 30');
                blankSvg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
                blankSvg.appendChild(selectedState.cloneNode(true));
                // tier.appendChild(selectedState);
                selectedState.classList.remove('selected');
                updateMinimap(selectedState.id, tier.getAttribute('data-tier'));
                selectedState = null;
            }
        });
    });

});