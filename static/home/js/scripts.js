const $ = document
let loadingElement = $.querySelector('#svgWrapper')

let urlForm = $.querySelector('.url-form')
let urlInput = $.querySelector('.url-input')

scraperInfoContainer = $.querySelector('#scraper-info')

function playLoading() {
    loadingElement.classList.remove('d-none')
}

function pauseLoading() {
    loadingElement.classList.add('d-none')
}

urlForm.addEventListener('submit', async event => {
    event.preventDefault();
    let urlValue = urlInput.value;
    var csrfToken = $.getElementsByName('csrfmiddlewaretoken')[0].value

    scraperInfoContainer.innerHTML = ''
    playLoading();
    
    try {
        let data = await RequestToReconServer(urlValue , csrfToken);
        if (data['status']) {
            insertTabsToHtml(data);
        }
        else{
            console.error(data)
            insertErrorToHtml('Some error occurred ! try again later')
        }
    } catch (error) {
        insertErrorToHtml('Could not connect to server :(')
        console.error(error)
    } finally {
        pauseLoading();
    }
});

class HttpError extends Error {
    constructor(status, statusText) {
        super(`HTTP Error: ${status} - ${statusText}`);
        this.status = status;
        this.statusText = statusText;
    }
}

async function RequestToReconServer(url , csrfToken) {
    try {
        let response = await fetch(`${location.origin}/api/v1/get-site-data/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken' : csrfToken
            },
            body: JSON.stringify({'url': url})
        });
        let data = await response.json()

        if (!response.ok) {
            data['status'] = false
            return data
        }

        data['status'] = true
        return data;

    } catch (error) {
        throw error;
    }
}


function insertErrorToHtml(error) {
    scraperInfoContainer.insertAdjacentHTML('afterbegin', `
    <p class="text-danger h3 text-break">${error}</p>`
  )
  pauseLoading()
}

function insertTabsToHtml(data) {

    scraperInfoContainer.insertAdjacentHTML('afterbegin', `
    <ul class="nav nav-tabs" id="myTab" role="tablist">
    <li class="nav-item" role="presentation">
      <button class="nav-link active" id="informations-tab" data-bs-toggle="tab" data-bs-target="#informations" type="button" role="tab" aria-controls="informations" aria-selected="true">Informations</button>
    </li>
    <li class="nav-item" role="presentation">
      <button class="nav-link" id="technologies-tab" data-bs-toggle="tab" data-bs-target="#technologies" type="button" role="tab" aria-controls="technologies" aria-selected="false">Technologies</button>
    </li>
    <li class="nav-item" role="presentation">
      <button class="nav-link" id="links-tab" data-bs-toggle="tab" data-bs-target="#links" type="button" role="tab" aria-controls="links" aria-selected="false">Links</button>
    </li>
    <li class="nav-item" role="presentation">
      <button class="nav-link" id="files-tab" data-bs-toggle="tab" data-bs-target="#files" type="button" role="tab" aria-controls="files" aria-selected="false">Files</button>
    </li>
    <li class="nav-item" role="presentation">
      <button class="nav-link" id="subdomains-tab" data-bs-toggle="tab" data-bs-target="#subdomains" type="button" role="tab" aria-controls="subdomains" aria-selected="false">Subdomains</button>
    </li>
  </ul>
  <div class="tab-content pt-4" id="myTabContent">
    <div class="tab-pane fade show active" id="informations" role="tabpanel" aria-labelledby="informations-tab">${insertInformation(data)}</div>
    <div class="tab-pane fade" id="technologies" role="tabpanel" aria-labelledby="technologies-tab">${insertTechnologies(data)}</div>
    <div class="tab-pane fade accordion" id="links" role="tabpanel" aria-labelledby="links-tab">${insertLinks(data)}</div>
    <div class="tab-pane fade accordion" id="files" role="tabpanel" aria-labelledby="files-tab">${insertFiles(data)}</div>
    <div class="tab-pane fade flex-wrap" id="subdomains" role="tabpanel" aria-labelledby="subdomains-tab">${insertSubdomains(data)}</div>
  </div>`
  )
}

function insertInformation(data) {
    var mainInformations = data['Informations']
    var screenshoot = data['Screenshot']
    var ports = data['Ports']

    var elementBox = `
    <div class="row justify-content-center flex-wrap-reverse">
        <div class="col-12 col-lg-6 col-xxl-8">
            ${insertInformationLoop(informations = mainInformations , ports = ports , domain = data['domain'])}
        </div>
        <div class="col-12 col-sm-10 col-md-8 col-lg-6 col-xxl-4">
            <img src="${screenshoot ? screenshoot : '/media/screenshoots/default.png'}" alt="${data['url']}" class="w-100 screenshoopt-img">
            <p class="text-center text-muted">${data['url']}</p>
        </div>
    </div>
    `

    function insertInformationLoop(informations , ports , domain) {
        divElement =  `
        <li class="information-list">
            <p class="title">domain : </p>
            <div class="description">
                <p>${domain}</p>
            </div>
        </li>`
        informations['ports'] = ports

        if (! informations || informations.length <1 ) {
            divElement += `
            <p class="h4 text-danger">Information could not be loaded , try again later</p>`
        }
        else {
            for (item in informations) {
                divElement += `
                <li class="information-list">
                    <p class="title">${item} : </p>
                    <div class="description">
                        <p>${informations[item].join(' <span class="text-danger"> / </span> ')}</p>
                    </div>
                </li>`
            }
        }

        return divElement
    }

    return elementBox
}

function insertTechnologies(data) {
    var technologies = data['Technologies']
    var elementBox = ``
    if (!technologies){
        elementBox = `
        <div class="row justify-content-center pt-2 flex-wrap-reverse">
            <p class="text-danger h4">could not load technologies</p>
        </div>
        `
        return elementBox
    }
    else if (technologies.length <1){
        elementBox = `
        <div class="row justify-content-center pt-2 flex-wrap-reverse">
            <p class="text-danger h4">No technology found !</p>
        </div>
        `
    }
    else {
        for (techno in technologies) {
            elementBox += `
            <li class="position-relative w-fit pe-4 technology-list">
                <p class="align-self-end m-0 fw-bold">${techno}</p>
                <span class="version-badge badge bg-warning text-dark">
                ${technologies[techno].versions.length >0 ? technologies[techno].versions.join('  ,  ')  : '?'}
                </span>
            </li>
            `
        }
    }
    return elementBox
}

function insertLinks(data) {
    var links = data['Links']
    var elementBox = ``
    var count = 0
    if (! links) {
        elementBox += `
        <p class="text-danger h4">Can not load links</p>
        `
    }
    else if (links.length <1){
        elementBox += `
        <p class="text-danger h4">No links found !</p>
        `
    }
    else {
        for (link in links) {
            if (links[link].length <=1){
                continue
            }
            elementBox += `
            <div class="accordion-item">
            <h2 class="accordion-header" id="panelsStayOpen-headingOne">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#open-link_${count}" aria-expanded="true" aria-controls="open-link_${count}">
              <a class="align-self-end m-0 fw-bold text-break" href="${link}" target="_blank">${link}</a>
              </button>
            </h2>
            <div id="open-link_${count}" class="accordion-collapse collapse" aria-labelledby="panelsStayOpen-headingOne">
              <div class="accordion-body">
                ${linkedInLink(links[link])}
              </div>
            </div>
          </div>
            `
            function linkedInLink (links) {
                var data = ``
                 links.forEach(link => {
                     data += `
                     <li class="site-link">
                         <a class="align-self-end m-0 fw-bold text-break" href="${link}" target="_blank">${link}</a>
                     </li>
                     `
                 })
                return data
            }
            count += 1
        }
    }

    return elementBox
}

function insertFiles(data) {
    files = data['Files']
    var elementBox = ``
    if (!files) {
        elementBox +=`
        <p class="text-danger h4">Can not load files</p>
        `
    }
    else if (files.length <1){
        elementBox += `
        <p class="text-danger h4">No Files found !</p>
        `
    }
    else {
        var count = 0
        for (file in files) {
            if (files[file].length <=1){
                continue
            }
            elementBox += `
            <div class="accordion-item">
            <h2 class="accordion-header" id="panelsStayOpen-headingOne">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#open-file_${count}" aria-expanded="true" aria-controls="open-file_${count}">
                <b class="fw-bold m-0 text-break">${file}</b>
              </button>
            </h2>
            <div id="open-file_${count}" class="accordion-collapse collapse" aria-labelledby="panelsStayOpen-headingOne">
              <div class="accordion-body">
                ${fileInFile(files[file])}
              </div>
            </div>
          </div>
            `
            function fileInFile (files) {
                var data = ``
                 files.forEach(file => {
                     data += `
                     <li class="site-file">
                         <a class="align-self-end m-0 fw-bold text-break" href="${file}" target="_blank">${file}</a>
                     </li>
                     `
                 })
                return data
            }
            count += 1
        }
    }
    return elementBox
}

function insertSubdomains(data) {
    subdomains = data['Subdomains']
    var elementBox = ``
    if (!subdomains) {
        elementBox += `
        <p class="text-danger h4">can not load subdomains</p>
        `
    }
    else if (subdomains.length <=0){
        elementBox += `
        <p class="text-danger h4">No subdomain found !</p>
        `
    }
    else {
        for (subdomain in subdomains){
            elementBox +=`
            <div class="subdomain-container col-12 col-sm-10 col-md-6 col-lg-5 col-xl-4 col-xxl-3">
                <li>
                    <p class="fw-bold d-inline-block">Subdomain :</p>
                    <p class="d-inline-block">${subdomains[subdomain]['Subdomain name']}</p>
                </li>

                <li>
                    <p class="fw-bold d-inline-block">Status :</p>
                    <p class="d-inline-block">${subdomains[subdomain]['Status']}</p>
                </li>

                <li>
                    <p class="fw-bold d-inline-block">Title :</p>
                    <p class="d-inline-block">${subdomains[subdomain]['Title']}</p>
                </li>

                <li>
                    <p class="fw-bold d-inline-block">Emails :</p>
                    <p class="d-inline-block">${subdomains[subdomain]['Emails'].length > 1 ? subdomains[subdomain]['Emails'].join(' <span class="text-danger"> / </span> ') : 'No email found'}</p>
                </li>

                <li>
                    <p class="fw-bold d-inline-block">Phone numbers :</p>
                    <p class="d-inline-block">${subdomains[subdomain]['Phone numbers'].length >1 ? subdomains[subdomain]['Phone numbers'].join(' <span class="text-danger"> , </span> ') : 'No phone number found' }</p>
                </li>
            </div>
            `
        }
    }
    return elementBox
}