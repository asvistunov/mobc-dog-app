import json
import docker
import logging

from pathlib import Path
from docker.errors import APIError, ContainerError
from docker.types.services import Mount

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = docker.from_env()

mount = Mount(
    '/mobc-dog-clinic-testing/results/',
    # Absolute path to results dir
    (Path(__file__).parent / 'results').absolute().as_posix(),
    type='bind'
)

try:
    network = client.networks.create('dog-clinic-app-network', check_duplicate=True)
except APIError:
    network = client.networks.get('dog-clinic-app-network')

logger.info('Created dog-clinic-app-network network.')

with open('app_urls.json', 'r') as app_urls_file:
    app_urls = json.load(app_urls_file)


for app in app_urls['students_apps']:

    testing_images = {}

    for url_type in ['github', 'url']:

        logger.info(f'Started building testing image for {url_type}.')
        testing_image, _ = client.images.build(
            path='docker/app-testing/',
            tag=f'{url_type}_clinic-app-testing',
            buildargs={
                'APP_URL': app[url_type] if url_type == 'url' else 'http://clinic-app:80'
            }
        )
        logger.info(f'Finished building testing image for {url_type}.')

        testing_images[url_type] = testing_image

    logger.info(f'Started building app image from {app["github"]}')

    app_image, _ = client.images.build(
        path='docker/app-hosting/',
        buildargs={
            'GITHUB_REPO_URL': app['github']
        },
        tag='clinic-app'
    )
    logger.info(f'Finished building app image')

    app_container = client.containers.run(
        app_image.id,
        network=network.id, 
        name='clinic-app',
        detach=True
    )
    logger.info(f'Running app image from {app["github"]}')

    for image_type in testing_images:

        try:
            logger.info(f'Started tests for {app["student_id"]} {image_type} image')
            client.containers.run(
                testing_images[image_type].id,
                command=f'pytest /mobc-dog-clinic-testing/api_testing.py --no-header --no-summary  -q --json-report --json-report-file /mobc-dog-clinic-testing/results/{app["student_id"]}/{image_type}-report.json --json-report-omit warnings',
                network=network.id,
                name='clinic-app-testing',
                mounts=[mount],
                remove=True
            )

            logger.info('All tests have passed.')

        except ContainerError:
            logger.warning('Some tests have failed.')
        # else:
            # raise RuntimeError('Some ditch has happened /( ⁄•⁄-⁄•⁄ )/')


    app_container.kill()
    app_container.remove()
