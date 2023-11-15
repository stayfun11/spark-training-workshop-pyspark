"""Module to store configuration related objects."""
import typing as T
from pathlib import Path

import omegaconf as oc
from cloudpathlib import AnyPath


class ConfigLoader:  # pylint: disable=too-few-public-methods
    """A utility class for loading configuration files from a directory.

    The `ConfigLoader` class provides methods for loading configuration files from a directory
    using the OmegaConf library. It supports any path format supported by the `cloudpathlib`
    library. If you specify a non-null base confs directory, the final configuration will be
    the merge of the base configuration and the configuration in the confs directory.

    Attributes:
        confs_dir (AnyPath): The path of the directory containing the configuration files.

    Args:
        confs_dir (Union[str, Path]): The path of the directory containing the configuration files.
            Can be any path format supported by `cloudpathlib`.

    Methods:
        get(file_name: str) -> Dict[str, Any]: Load the specified config file.

    Examples:
        To load a configuration from a file named 'config.yaml' located in a directory '/path/to/configs/dev',
        and a file named 'config.yaml' located in a directory '/path/to/configs/base', use the following code:
        >>> from dps_my_project_pyspark.config import ConfigLoader
        >>> loader = ConfigLoader(confs_dir='/path/to/configs', env='dev')
        >>> config = loader.get('config.yaml')  #
    """

    def __init__(
        self, confs_dir: T.Union[str, Path] = "confs", env: str = "local", base_env: T.Optional[str] = "base"
    ) -> None:
        """Init the ConfigLoader.

        Args:
            confs_dir:
                The paths of the directory containing the conf files.
                Can be any path supported by
                (cloudpathlib)[https://cloudpathlib.drivendata.org/stable/]
            env:
                The name of the environment to load the configuration files from.
                Must be a subdirectory of ``confs_dir``.
            base_env:
                The name of the base environement to load the base configuration files from.
                Must be a subdirectory of ``confs_dir``.
                If None, no base configuration will be loaded.
        """
        self.confs_dir = AnyPath(confs_dir)
        self.env = env
        self.base_env = base_env

    @T.no_type_check  # Cloudpath does not provide typing
    def get(self, file_name: str) -> T.Dict[str, T.Any]:
        """Load the specified config file.

        The config file will be a merge of the file based on the environment and the base environment,
        the values in the environment file will overwrite the values in the base environment file
        if they have the same key.

        Args:
            file_name:
                The name of the file to load.
                File must be in ``self.confs_dir`` directory
        """
        env_file = self.confs_dir / self.env / file_name
        base_env_file = self.confs_dir / self.base_env / file_name if self.base_env else None

        if not env_file.is_file() and not base_env_file.is_file():
            raise FileNotFoundError(
                f"Neither {env_file} nor {base_env_file} exist."
                f"To load '{file_name}', it must exist in either the base env or the env directory."
            )

        if env_file.is_file():
            env_conf = self._get_one(env_file)
        else:
            env_conf = {}

        if base_env_file and base_env_file.is_file():
            base_env_conf = self._get_one(base_env_file)
        else:
            base_env_conf = {}

        conf = {**base_env_conf, **env_conf}
        # By default, OmegaConf will return container types (e.g. ListConfig), which are non python native objects.
        # While this is convenient, it can cause issues when passing the config to other libraries.
        # In particular, this does not work well with the pyspark library.
        # To avoid this, we convert the config to a python native object.
        # See https://github.com/omry/omegaconf/discussions/848
        native_objects_conf = oc.OmegaConf.to_object(oc.DictConfig(conf))
        return native_objects_conf

    @T.no_type_check  # Cloudpath does not provide typing
    def _get_one(self, file_path: AnyPath) -> T.Dict[str, T.Any]:
        """Load the specified config file in the given environment.

        Args:
            file_path:
                The path of the file to load.
        """
        # pylint: disable=no-member
        text = file_path.read_text()
        conf = oc.OmegaConf.create(text)
        return conf
