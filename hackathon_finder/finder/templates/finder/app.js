
    document.addEventListener('DOMContentLoaded', function () {
        // Debug configuration
        const DEBUG_MODE = true; // Set to false in production

        // Initialize hidden selects when page loads
        updateHiddenSelects();
        
        // Initialize existing selections
        initializeExistingSelections();

        // Skill tag removal
        document.querySelectorAll('#skills-tags .remove-tag').forEach(tag => {
            tag.addEventListener('click', function () {
                const skillId = this.getAttribute('data-id');
                removeItemFromSelect('id_skills', skillId);
                
                // Remove from display with animation
                const tagElement = this.parentElement;
                animateAndRemove(tagElement, () => updateHiddenSelects());
            });
        });

        // Tech stack tag removal
        document.querySelectorAll('#tech-tags .remove-tag').forEach(tag => {
            tag.addEventListener('click', function () {
                const techId = this.getAttribute('data-id');
                removeItemFromSelect('id_tech_stack', techId);
                
                // Remove from display with animation
                const tagElement = this.parentElement;
                animateAndRemove(tagElement, () => updateHiddenSelects());
            });
        });

        // Hackathon removal
        document.querySelectorAll('#hackathon-list .remove-hackathon').forEach(btn => {
            btn.addEventListener('click', function () {
                const hackathonId = this.getAttribute('data-id');
                removeItemFromSelect('id_interested_hackathons', hackathonId);
                
                // Remove from display with animation
                const hackathonItem = this.closest('.hackathon-item');
                animateAndRemove(hackathonItem, () => updateHiddenSelects());
            });
        });

        // Add new skill functionality
        document.getElementById('add-skill-btn')?.addEventListener('click', function () {
            const skillInput = document.getElementById('id_new_skills');
            if (skillInput && skillInput.value.trim() !== '') {
                const skills = skillInput.value.trim().split(',').map(s => s.trim()).filter(s => s !== '');
                
                skills.forEach(skill => {
                    // Create a temporary ID for new skills
                    const tempId = 'new-skill-' + Date.now() + '-' + Math.random().toString(36).substr(2, 5);
                    
                    // Create and add new skill tag
                    const newSkill = document.createElement('span');
                    newSkill.className = 'bg-gradient-to-r from-accent-blue/20 to-accent-blue/30 text-accent-blue px-3 py-1.5 rounded-full text-sm font-medium flex items-center gap-2 border border-accent-blue/20';
                    newSkill.innerHTML = `
                        ${skill} 
                        <span class="remove-tag cursor-pointer hover:bg-accent-blue/20 rounded-full w-5 h-5 flex items-center justify-center transition-all" 
                              data-id="${tempId}" 
                              data-name="${skill}">×</span>
                    `;
                    
                    document.getElementById('skills-tags').appendChild(newSkill);
                    
                    // Add to hidden select
                    addToSelect('id_skills', tempId, skill, true);
                    
                    // Setup removal
                    setupTagRemoval(newSkill, 'id_skills', tempId);
                });
                
                // Clear input and update selects
                skillInput.value = '';
                updateHiddenSelects();
            }
        });

        // Add new tech functionality
        document.getElementById('add-tech-btn')?.addEventListener('click', function () {
            const techInput = document.getElementById('id_new_tech_stack');
            if (techInput && techInput.value.trim() !== '') {
                const techs = techInput.value.trim().split(',').map(t => t.trim()).filter(t => t !== '');
                
                techs.forEach(tech => {
                    // Create a temporary ID for new tech
                    const tempId = 'new-tech-' + Date.now() + '-' + Math.random().toString(36).substr(2, 5);
                    
                    // Create and add new tech tag
                    const newTech = document.createElement('span');
                    newTech.className = 'bg-gradient-to-r from-purple-500/20 to-purple-600/30 text-purple-400 px-3 py-1.5 rounded-full text-sm font-medium flex items-center gap-2 border border-purple-500/20';
                    newTech.innerHTML = `
                        ${tech} 
                        <span class="remove-tag cursor-pointer hover:bg-purple-500/20 rounded-full w-5 h-5 flex items-center justify-center transition-all" 
                              data-id="${tempId}" 
                              data-name="${tech}">×</span>
                    `;
                    
                    document.getElementById('tech-tags').appendChild(newTech);
                    
                    // Add to hidden select
                    addToSelect('id_tech_stack', tempId, tech, true);
                    
                    // Setup removal
                    setupTagRemoval(newTech, 'id_tech_stack', tempId);
                });
                
                // Clear input and update selects
                techInput.value = '';
                updateHiddenSelects();
            }
        });

        // Add new hackathon functionality
        document.getElementById('add-hackathon-btn')?.addEventListener('click', function () {
            const nameInput = document.getElementById('id_hackathon_name');
            if (nameInput && nameInput.value.trim() !== '') {
                // Create a unique ID for this hackathon
                const hackathonId = 'new-hack-' + Date.now() + '-' + Math.random().toString(36).substr(2, 5);
                
                const levelSelect = document.getElementById('id_hackathon_level');
                const dateInput = document.getElementById('id_hackathon_date');
                const descInput = document.getElementById('id_hackathon_description');
                const locationInput = document.getElementById('id_hackathon_location');
                
                const levelText = levelSelect?.options[levelSelect.selectedIndex]?.text || '';
                const today = new Date();
                const eventDate = dateInput.value ? new Date(dateInput.value) : today;
                
                // Determine if it's upcoming based on date
                const badgeClass = eventDate >= today ?
                    'bg-green-500/20 text-green-400 border border-green-500/20' :
                    'bg-purple-500/20 text-purple-400 border border-purple-500/20';
                const badgeText = eventDate >= today ? 'Upcoming' : 'Current';
                
                // Create new hackathon item
                const newHackathon = document.createElement('div');
                newHackathon.className = 'bg-gradient-to-r from-dark-800 to-dark-900 p-4 rounded-lg border border-gray-800 shadow-md hackathon-item opacity-0';
                newHackathon.innerHTML = `
                    <div class="flex justify-between">
                        <div class="flex items-center gap-3">
                            <span class="font-medium text-white">${nameInput.value.trim()}</span>
                            <span class="text-xs px-3 py-1 rounded-full bg-accent-blue/20 text-accent-blue border border-accent-blue/20">
                                ${levelText}
                            </span>
                            <span class="text-xs px-3 py-1 rounded-full ${badgeClass}">
                                ${badgeText}
                            </span>
                        </div>
                        <div class="flex items-center gap-4">
                            <span class="text-sm text-gray-400">${dateInput.value || 'No date specified'}</span>
                            <button type="button" class="text-red-400 hover:text-red-300 remove-hackathon" data-id="${hackathonId}">
                                <i class="fas fa-times"></i>
                            </button>
                        </div>
                    </div>
                    <p class="text-sm text-gray-300 mt-2">${descInput.value || 'No description provided'}</p>
                    <div class="flex gap-2 mt-3">
                        <span class="text-xs px-2 py-1 rounded-full bg-dark-700 text-gray-400">
                            <i class="fas fa-map-marker-alt mr-1"></i> Location: ${locationInput.value || 'Online'}
                        </span>
                    </div>
                `;
                
                document.getElementById('hackathon-list').appendChild(newHackathon);
                
                // Add to hidden select
                addToSelect('id_interested_hackathons', hackathonId, nameInput.value.trim(), true);
                
                // Setup removal
                const removeBtn = newHackathon.querySelector('.remove-hackathon');
                removeBtn.addEventListener('click', function() {
                    removeItemFromSelect('id_interested_hackathons', hackathonId);
                    animateAndRemove(newHackathon, () => updateHiddenSelects());
                });
                
                // Animate in
                setTimeout(() => {
                    newHackathon.classList.remove('opacity-0');
                }, 10);
                
                // Clear inputs and update selects
                if (nameInput) nameInput.value = '';
                if (levelSelect) levelSelect.selectedIndex = 0;
                if (dateInput) dateInput.value = '';
                if (descInput) descInput.value = '';
                if (locationInput) locationInput.value = '';
                
                updateHiddenSelects();
            }
        });

        // Profile picture preview
        const profilePicInput = document.getElementById('{{ form.profile_picture.id_for_label }}');
        if (profilePicInput) {
            profilePicInput.addEventListener('change', function () {
                if (this.files && this.files[0]) {
                    const reader = new FileReader();
                    
                    reader.onload = function (e) {
                        const profileImg = document.querySelector('.rounded-full');
                        if (profileImg) {
                            if (profileImg.tagName === 'IMG') {
                                profileImg.src = e.target.result;
                            } else {
                                // If using the placeholder div, replace with img
                                const newImg = document.createElement('img');
                                newImg.src = e.target.result;
                                newImg.className = 'rounded-full mx-auto object-cover border-4 border-accent-blue/40 blue-glow shadow-lg';
                                newImg.width = 180;
                                newImg.height = 180;
                                newImg.alt = 'Profile picture';
                                
                                profileImg.parentNode.replaceChild(newImg, profileImg);
                            }
                        }
                    }
                    
                    reader.readAsDataURL(this.files[0]);
                }
            });
        }

        // Form validation with nice animations
        const form = document.querySelector('form');
        if (form) {
            form.addEventListener('submit', function (e) {
                // Update hidden selects before validation
                updateHiddenSelects();
                
                // Debug form data before submission
                debugFormData();
                
                let isValid = true;
                const requiredFields = form.querySelectorAll('input[required], textarea[required], select[required]');
                
                requiredFields.forEach(field => {
                    if (!field.value.trim()) {
                        isValid = false;
                        field.classList.add('border-red-500', 'shake-animation');
                        
                        // Add error message
                        const errorMsg = document.createElement('p');
                        errorMsg.className = 'text-red-500 text-xs mt-1 error-message';
                        errorMsg.textContent = 'This field is required';
                        
                        // Remove any existing error message
                        const existingError = field.parentNode.querySelector('.error-message');
                        if (existingError) {
                            existingError.remove();
                        }
                        
                        field.parentNode.appendChild(errorMsg);
                        
                        // Remove shake animation after it completes
                        setTimeout(() => {
                            field.classList.remove('shake-animation');
                        }, 500);
                    } else {
                        field.classList.remove('border-red-500');
                        const existingError = field.parentNode.querySelector('.error-message');
                        if (existingError) {
                            existingError.remove();
                        }
                    }
                });
                
                if (!isValid) {
                    e.preventDefault();
                    // Scroll to first error
                    const firstError = form.querySelector('.border-red-500');
                    if (firstError) {
                        firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                }
            });
        }

        // Helper functions
        function initializeExistingSelections() {
            // Initialize existing skills
            {% for skill in user.profile.skills.all %}
                const skillOption = document.querySelector(`#id_skills option[value="{{ skill.id }}"]`);
                if (skillOption) skillOption.selected = true;
            {% endfor %}
            
            // Initialize existing tech stack
            {% for tech in user.profile.tech_stack.all %}
                const techOption = document.querySelector(`#id_tech_stack option[value="{{ tech.id }}"]`);
                if (techOption) techOption.selected = true;
            {% endfor %}
            
            // Initialize existing hackathons
            {% for hackathon in user.profile.interested_hackathons.all %}
                const hackOption = document.querySelector(`#id_interested_hackathons option[value="{{ hackathon.id }}"]`);
                if (hackOption) hackOption.selected = true;
            {% endfor %}
        }

        function addToSelect(selectId, value, text, selected = false) {
            const select = document.getElementById(selectId);
            if (select) {
                const option = document.createElement('option');
                option.value = value;
                option.textContent = text;
                option.selected = selected;
                if (value.startsWith('new-')) {
                    option.setAttribute('data-temp', 'true');
                }
                select.appendChild(option);
            }
        }

        function removeItemFromSelect(selectId, value) {
            const select = document.getElementById(selectId);
            if (select) {
                const option = select.querySelector(`option[value="${value}"]`);
                if (option) option.remove();
            }
        }

        function animateAndRemove(element, callback) {
            element.classList.add('scale-0', 'opacity-0');
            setTimeout(() => {
                element.remove();
                if (callback) callback();
            }, 200);
        }

        function setupTagRemoval(tagElement, selectId, value) {
            const removeBtn = tagElement.querySelector('.remove-tag');
            if (removeBtn) {
                removeBtn.addEventListener('click', function() {
                    removeItemFromSelect(selectId, value);
                    animateAndRemove(tagElement, () => updateHiddenSelects());
                });
            }
        }

        // Function to update all hidden select fields
        function updateHiddenSelects() {
            debugLog('Updating hidden selects...');
            
            // Skills
            const skillsSelect = document.getElementById('id_skills');
            if (skillsSelect) {
                const skillTags = Array.from(document.querySelectorAll('#skills-tags > span')).map(span => 
                    span.querySelector('.remove-tag')?.getAttribute('data-id')
                ).filter(id => id !== undefined);
                
                debugLog('Processing skills:', skillTags);
                Array.from(skillsSelect.options).forEach(option => {
                    const wasSelected = option.selected;
                    option.selected = skillTags.includes(option.value);
                    if (wasSelected !== option.selected && DEBUG_MODE) {
                        debugLog(`Skill ${option.value} ${option.selected ? 'selected' : 'deselected'}`);
                    }
                });
            }

            // Tech Stack
            const techSelect = document.getElementById('id_tech_stack');
            if (techSelect) {
                const techTags = Array.from(document.querySelectorAll('#tech-tags > span')).map(span => 
                    span.querySelector('.remove-tag')?.getAttribute('data-id')
                ).filter(id => id !== undefined);
                
                debugLog('Processing tech stack:', techTags);
                Array.from(techSelect.options).forEach(option => {
                    const wasSelected = option.selected;
                    option.selected = techTags.includes(option.value);
                    if (wasSelected !== option.selected && DEBUG_MODE) {
                        debugLog(`Tech ${option.value} ${option.selected ? 'selected' : 'deselected'}`);
                    }
                });
            }

            // Hackathons
            const hackSelect = document.getElementById('id_interested_hackathons');
            if (hackSelect) {
                const hackTags = Array.from(document.querySelectorAll('#hackathon-list .hackathon-item')).map(item => 
                    item.querySelector('.remove-hackathon')?.getAttribute('data-id')
                ).filter(id => id !== undefined);
                
                debugLog('Processing hackathons:', hackTags);
                Array.from(hackSelect.options).forEach(option => {
                    const wasSelected = option.selected;
                    option.selected = hackTags.includes(option.value);
                    if (wasSelected !== option.selected && DEBUG_MODE) {
                        debugLog(`Hackathon ${option.value} ${option.selected ? 'selected' : 'deselected'}`);
                    }
                });
            }
        }

        // Debug function to check form data
        function debugFormData() {
            if (!DEBUG_MODE) return;
            
            console.group('Form Data Debug');
            
            // Skills
            const skills = Array.from(document.querySelectorAll('#skills-tags > span')).map(el => {
                return {
                    id: el.querySelector('.remove-tag')?.getAttribute('data-id'),
                    name: el.querySelector('.remove-tag')?.getAttribute('data-name'),
                    text: el.textContent.replace('×', '').trim()
                };
            });
            console.log('Skills:', skills);
            
            // Tech Stack
            const techStack = Array.from(document.querySelectorAll('#tech-tags > span')).map(el => {
                return {
                    id: el.querySelector('.remove-tag')?.getAttribute('data-id'),
                    name: el.querySelector('.remove-tag')?.getAttribute('data-name'),
                    text: el.textContent.replace('×', '').trim()
                };
            });
            console.log('Tech Stack:', techStack);
            
            // Hackathons
            const hackathons = Array.from(document.querySelectorAll('#hackathon-list .hackathon-item')).map(el => {
                return {
                    id: el.querySelector('.remove-hackathon')?.getAttribute('data-id'),
                    name: el.querySelector('.font-medium')?.textContent?.trim()
                };
            });
            console.log('Hackathons:', hackathons);
            
            // Hidden selects
            console.log('Skills Select:', Array.from(document.getElementById('id_skills').options)
                .filter(opt => opt.selected)
                .map(opt => opt.value));
            
            console.log('Tech Stack Select:', Array.from(document.getElementById('id_tech_stack').options)
                .filter(opt => opt.selected)
                .map(opt => opt.value));
            
            console.log('Hackathons Select:', Array.from(document.getElementById('id_interested_hackathons').options)
                .filter(opt => opt.selected)
                .map(opt => opt.value));
            
            console.groupEnd();
        }

        // Add debug button to the page
        function addDebugButton() {
            if (!DEBUG_MODE) return;
            
            const debugBtn = document.createElement('button');
            debugBtn.textContent = 'Debug Form';
            debugBtn.className = 'fixed bottom-4 right-4 bg-blue-500 text-white px-4 py-2 rounded-full shadow-lg z-50';
            debugBtn.onclick = debugFormData;
            
            document.body.appendChild(debugBtn);
        }

        // Initialize debug button
        addDebugButton();
    });