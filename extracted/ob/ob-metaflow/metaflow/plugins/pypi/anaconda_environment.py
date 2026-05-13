from .conda_environment import CondaEnvironment


# To placate people who don't want to see a shred of conda in UX, we symlink
# --environment=pypi to --environment=conda
class AnacondaEnvironment(CondaEnvironment):
    TYPE = "anaconda"

    def decospecs(self):
        return ("anaconda",)
