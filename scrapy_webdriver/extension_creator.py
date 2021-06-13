from zipfile import ZipFile

def create_extension(username, password):
    with open('extension/background.js', 'w') as file:
        text = """
                function callbackFn(details) {
                    return {
                        authCredentials: {
                            username: "%s",
                            password: "%s"
                        }
                    };
                }
                
                browser.webRequest.onAuthRequired.addListener(
                        callbackFn,
                        {urls: ["<all_urls>"]},
                        ['blocking']
                );
               """ % (username, password)
        file.write(text)
    zip_file = ZipFile('extensions/extension.xpi', 'w')
    zip_file.write('extension/background.js', arcname='background.js')
    zip_file.write('extension/manifest.json', arcname='manifest.json')
    zip_file.close()

if __name__ == '__main__':
    pass
