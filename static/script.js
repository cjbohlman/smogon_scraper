window.addEventListener('DOMContentLoaded', () => {
    let submit_btn = document.getElementById('url-submit');
    let raw_data_btn = document.getElementById('raw-link');
    let description_box = document.querySelector('.results');

    submit_btn.addEventListener('click', () => {
        description_box.innerHTML = "Loading...";

        // get data from text box
        let call_params = document.getElementById('url-input').value;
        
        // run an api call and populate box with api call results
        getAPICall(call_params).then((strategies) => {
            if (strategies === null) {
                description_box.innerHTML = "No strategies found.";
                return;
            }
            const formatted_strategies = JSON.stringify(strategies,null,4); 
            description_box.innerHTML = "<pre>"+formatted_strategies+"</pre>";
        });        
    });

    raw_data_btn.addEventListener('click', () => {
        let call_params = document.getElementById('url-input').value;
        window.open(window.location.href + 'pkmn/' + call_params);
    });
});

async function getAPICall(call_params) {
    const smogon_url = window.location.href + 'pkmn/';
    const response = await fetch(smogon_url + call_params);
    const strategies = await response.json();
    return strategies;
}