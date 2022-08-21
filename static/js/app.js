(function () {
    'use strict'
    var input_form = document.querySelector('form')
    var url_field = document.querySelector('#url-field')
    var yt_select = document.querySelector('#yt-select')
    var ml_select = document.querySelector('#ml-select')
    var submit_button = document.querySelector('#submit')
    var transcript = document.querySelector('#transcript')
    const alertPlaceholder = document.getElementById('liveAlertPlaceholder')
    const alert = (message, type) => {
        const wrapper = document.createElement('div')
        wrapper.innerHTML = [
            `<div class="alert alert-${type} alert-dismissible" role="alert">`,
            `   <div>${message}</div>`,
            '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
            '</div>'
        ].join('')

        alertPlaceholder.append(wrapper)
    }

    yt_select.disabled = true
    ml_select.disabled = true
    submit_button.disabled = true
    url_field.addEventListener('input', async function (event) {
        if (url_field.checkValidity()) {
            submit_button.innerHTML = `<span class="spinner-border spinner-border-sm"></span>`
            let response = await fetch('/tracks', {
                method: 'POST',
                body: new URLSearchParams("url=" + url_field.value)
            })
            submit_button.innerHTML = `<i class="fa-solid fa-brain"></i>`
            if(!response.ok) {
                alert('Something went wrong: '+response.status+' '+response.statusText, 'danger')
            }
            else {
                let dt = await response.json()
                if (dt['success']) {
                    for (let i = 0; i < dt['yt_tracks'].length; i++) {
                        let opt = dt['yt_tracks'][i]
                        yt_select.add(new Option(opt['label'], opt['value']))
                    }
                    for (let i = 0; i < dt['ml_tracks'].length; i++) {
                        let opt = dt['ml_tracks'][i]
                        ml_select.add(new Option(opt['label'], opt['value']))
                    }
                    yt_select.disabled = false
                    ml_select.disabled = false
                    submit_button.disabled = false
                    url_field.disabled = true
                    transcript.classList.toggle('transcript-placeholder-1')
                    transcript.style.backgroundImage = 'url("' + dt['thumbnail'] + '")'
                }
                else {
                    alert(dt['error'], 'danger')
                }
            }
        }
    })
    input_form.addEventListener('submit', async function (event) {
        event.preventDefault()
        event.stopPropagation()
        if (input_form.checkValidity()) {
            yt_select.disabled = true
            ml_select.disabled = true
            submit_button.disabled = true
            submit_button.innerHTML = `<span class="spinner-border spinner-border-sm"></span>`
            let response = await fetch('/transcript', {
                method: 'POST',
                body: new URLSearchParams('url=' + url_field.value + '&yt=' + yt_select.value + '&ml=' + ml_select.value)
            })
            if(!response.ok) {
                alert('Something went wrong: '+response.status+' '+response.statusText, 'danger')
            }
            else {
                let tr = await response.json()
                if (tr['success']) {
                    transcript.classList.toggle('transcript-placeholder-2')
                    transcript.innerHTML = tr['transcript']
                }
                else {
                    alert(tr['error'], 'danger')
                }
            }
            submit_button.innerHTML = `<i class="fa-solid fa-brain"></i>`
            yt_select.disabled = false
            ml_select.disabled = false
            submit_button.disabled = false
        }
    })
})()