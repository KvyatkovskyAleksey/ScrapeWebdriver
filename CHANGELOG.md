v1.0 
- Moved selenium version to 4
- Added tests
- Use poetry for dependency management

v1.0.1
- fix default kwargs on SeleniumRequest

v1.0.2
- fix http / https proxies logic

v1.0.3
- fix parsing of proxies without credentials

v1.0.4
- updated error handling on driver errors

v1.0.5
- disable "places.history.enabled" for prevent memory issues
- added logic for reload driver instance after 50 urls for prevent memory issues

v1.0.6
- update logic for driver reloading
