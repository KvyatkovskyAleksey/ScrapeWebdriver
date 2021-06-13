import os
from zipfile import ZipFile

def create_extension(username, password):
    path = os.path.dirname(os.path.realpath(__file__))
    with open(f'{path}/extension/background.js', 'w') as file:
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
    zip_file = ZipFile(f'{path}/extensions/extension.xpi', 'w')
    zip_file.write(f'{path}/extension/background.js', arcname='background.js')
    zip_file.write(f'{path}/extension/manifest.json', arcname='manifest.json')
    zip_file.close()

if __name__ == '__main__':
    pass
