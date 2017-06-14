SearchEngines = {
    'google': 'https://www.google.com/search?q={0}&start={1}'
}


SearchEngineResultSelectors = {
    'google': {
        'search_result_main_block': '//div[@class="rc"]',
        'url_title_block': './/h3/a',
        'url': '@href',
        'title': './/span/text()',
        'description': './/div/div/span/span/text()',
        'images': '//div[@class="bicc"]/a/g-img/img[contains(@src, "jpeg")]/@src'
    }
}
