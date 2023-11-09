import schemathesis

from hypothesis import settings

from schemathesis.checks import status_code_conformance, \
    content_type_conformance, response_schema_conformance

with open('/mobc-dog-clinic-testing/app_url', 'r') as app_url_file:
    app_url = app_url_file.readline()

schema = schemathesis.from_path('/mobc-dog-clinic-testing/clinic.yaml', base_url=app_url)

@schema.parametrize(operation_id='root__get')
@settings(max_examples=1)
def test_root(case):
    response = case.call()

    case.validate_response(
        response,
        checks=(
            status_code_conformance,
            content_type_conformance,
            response_schema_conformance
        )
    )

@schema.parametrize(operation_id='get_post_post_post')
@settings(max_examples=1)
def test_post(case):
    response = case.call()

    case.validate_response(
        response,
        checks=(
            status_code_conformance, 
            content_type_conformance,
            response_schema_conformance
        )
    )

@schema.parametrize(endpoint='^/dog$')
@settings(max_examples=1)
def test_dog(case):
    response = case.call()

    case.validate_response(
        response,
        checks=(
            status_code_conformance,
            content_type_conformance,
            response_schema_conformance
        )
    )

def before_generate_path_parameters(context, strategy):
    available_default_keys = [0, 1, 2, 3, 4, 5, 6]
    return strategy.filter(lambda x: x['pk'] in available_default_keys)


@schema.hooks.apply(before_generate_path_parameters)
@schema.parametrize(endpoint='^/dog/')
@settings(max_examples=1)
def test_dog_by_pk(case):

    response = case.call()

    case.validate_response(
        response,
        checks=(
            status_code_conformance,
            content_type_conformance,
            response_schema_conformance
        )
    )
