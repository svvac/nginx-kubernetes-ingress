import requests
import pytest

from base64 import b64encode
from suite.fixtures import PublicEndpoint
from suite.resources_utils import create_secret_from_yaml, delete_secret, replace_secret, ensure_connection_to_public_endpoint, wait_before_test
from suite.resources_utils import create_items_from_yaml, delete_items_from_yaml, create_example_app, delete_common_app
from suite.resources_utils import wait_until_all_pods_are_ready, is_secret_present
from suite.yaml_utils import get_first_ingress_host_from_yaml
from settings import TEST_DATA

def to_base64(b64_string):
    return b64encode(
        b64_string.encode('ascii')
    ).decode('ascii')


class AuthBasicSecretsSetup:
    """
    Encapsulate Auth Basic Secrets Example details.

    Attributes:
        public_endpoint (PublicEndpoint):
        ingress_host (str):
        credentials (str):
    """
    def __init__(self, public_endpoint: PublicEndpoint, ingress_host, credentials):
        self.public_endpoint = public_endpoint
        self.ingress_host = ingress_host
        self.credentials = credentials


class AuthBasicSecret:
    """
    Encapsulate secret name for Auth Basic Secrets Example.

    Attributes:
        secret_name (str):
    """
    def __init__(self, secret_name):
        self.secret_name = secret_name


@pytest.fixture(scope="class", params=["standard", "mergeable"])
def auth_basic_secrets_setup(request, kube_apis, ingress_controller_endpoint, ingress_controller, test_namespace) -> AuthBasicSecretsSetup:
    with open(f"{TEST_DATA}/auth-basic-secrets/credentials/credentials.txt", "r") as credentials_file:
        credentials = credentials_file.read().replace('\n', '')
    print("------------------------- Deploy Auth Basic Secrets Example -----------------------------------")
    create_items_from_yaml(kube_apis, f"{TEST_DATA}/auth-basic-secrets/{request.param}/auth-basic-secrets-ingress.yaml", test_namespace)
    ingress_host = get_first_ingress_host_from_yaml(f"{TEST_DATA}/auth-basic-secrets/{request.param}/auth-basic-secrets-ingress.yaml")
    create_example_app(kube_apis, "simple", test_namespace)
    wait_until_all_pods_are_ready(kube_apis.v1, test_namespace)
    ensure_connection_to_public_endpoint(ingress_controller_endpoint.public_ip,
                                         ingress_controller_endpoint.port,
                                         ingress_controller_endpoint.port_ssl)

    def fin():
        print("Clean up the Auth Basic Secrets Application:")
        delete_common_app(kube_apis, "simple", test_namespace)
        delete_items_from_yaml(kube_apis, f"{TEST_DATA}/auth-basic-secrets/{request.param}/auth-basic-secrets-ingress.yaml",
                               test_namespace)

    request.addfinalizer(fin)

    return AuthBasicSecretsSetup(ingress_controller_endpoint, ingress_host, credentials)


@pytest.fixture
def auth_basic_secret(request, kube_apis, ingress_controller_endpoint, auth_basic_secrets_setup, test_namespace) -> AuthBasicSecret:
    secret_name = create_secret_from_yaml(kube_apis.v1, test_namespace, f"{TEST_DATA}/auth-basic-secrets/auth-basic-secret.yaml")
    wait_before_test(1)

    def fin():
        print("Delete Secret:")
        if is_secret_present(kube_apis.v1, secret_name, test_namespace):
            delete_secret(kube_apis.v1, secret_name, test_namespace)

    request.addfinalizer(fin)

    return AuthBasicSecret(secret_name)


@pytest.mark.ingresses
class TestAuthBasicSecrets:
    def test_response_code_200_and_server_name(self, auth_basic_secrets_setup, auth_basic_secret):
        req_url = f"http://{auth_basic_secrets_setup.public_endpoint.public_ip}:{auth_basic_secrets_setup.public_endpoint.port}/backend2"
        resp = requests.get(req_url, headers={"host": auth_basic_secrets_setup.ingress_host, "authorization": f"Basic {to_base64(auth_basic_secrets_setup.credentials)}"})
        assert resp.status_code == 200
        assert f"Server name: backend2" in resp.text

    # FIXME: for mergeable config, minion secrets seems to be ignored
    def test_response_codes_after_secret_remove_and_restore(self, kube_apis, auth_basic_secrets_setup, test_namespace, auth_basic_secret):
        req_url = f"http://{auth_basic_secrets_setup.public_endpoint.public_ip}:{auth_basic_secrets_setup.public_endpoint.port}/backend2"
        delete_secret(kube_apis.v1, auth_basic_secret.secret_name, test_namespace)
        wait_before_test(1)
        resp = requests.get(req_url, headers={"host": auth_basic_secrets_setup.ingress_host, "authorization": f"Basic {to_base64(auth_basic_secrets_setup.credentials)}"})
        assert resp.status_code == 403
        
        auth_basic_secret.secret_name = create_secret_from_yaml(kube_apis.v1, test_namespace, f"{TEST_DATA}/auth-basic-secrets/auth-basic-secret.yaml")
        wait_before_test(1)
        resp = requests.get(req_url, headers={"host": auth_basic_secrets_setup.ingress_host, "authorization": f"Basic {to_base64(auth_basic_secrets_setup.credentials)}"})
        assert resp.status_code == 200

    def test_response_code_403_with_invalid_secret(self, kube_apis, auth_basic_secrets_setup, test_namespace, auth_basic_secret):
        req_url = f"http://{auth_basic_secrets_setup.public_endpoint.public_ip}:{auth_basic_secrets_setup.public_endpoint.port}/backend2"
        replace_secret(kube_apis.v1, auth_basic_secret.secret_name, test_namespace, f"{TEST_DATA}/auth-basic-secrets/auth-basic-secret-invalid.yaml")
        wait_before_test(1)
        resp = requests.get(req_url, headers={"host": auth_basic_secrets_setup.ingress_host, "authorization": f"Basic {to_base64(auth_basic_secrets_setup.credentials)}"})
        assert resp.status_code == 403

    def test_response_code_302_with_updated_secret(self, kube_apis, auth_basic_secrets_setup, test_namespace, auth_basic_secret):
        req_url = f"http://{auth_basic_secrets_setup.public_endpoint.public_ip}:{auth_basic_secrets_setup.public_endpoint.port}/backend2"
        replace_secret(kube_apis.v1, auth_basic_secret.secret_name, test_namespace, f"{TEST_DATA}/auth-basic-secrets/auth-basic-secret-updated.yaml")
        wait_before_test(1)
        resp = requests.get(req_url, headers={"host": auth_basic_secrets_setup.ingress_host, "authorization": f"Basic {to_base64(auth_basic_secrets_setup.credentials)}"}, allow_redirects=False)
        #FIXME: is this test relevant ? Check data for updated secret: if you change the htpasswd this test resturns 401
        assert resp.status_code == 302
