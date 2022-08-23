version: '3.8'

services:
    probe:
        image: ${CI_REGISTRY_IMAGE}:${APP_VERSION}
        init: true
        ports: 
            - "8000:8000"
        deploy:
            mode: replicated
            restart_policy:
                condition: on-failure
            update_config:
                parallelism: 1
                failure_action: rollback
                delay: 15s
