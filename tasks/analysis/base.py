# -*- coding: utf-8 -*-

import os

import luigi
import law

import law.contrib.htcondor

class Task(law.Task):
    """
    Base task that we use to force a version parameter on all inheriting tasks, and that provides
    some convenience methods to create local file and directory targets at the default data path.
    """

    version = luigi.Parameter()

    def store_parts(self):
        return (self.__class__.__name__, self.version)

    def local_path(self, *path):
        # ANALYSIS_DATA_PATH is defined in setup.sh
        """
        TODO: ENV has to be updated!!!
        """
        parts = (os.getenv("ANALYSIS_DATA_PATH_TARGET"),) + self.store_parts() + path
        return os.path.join(*parts)

    def local_target(self, *path):
        return law.LocalFileTarget(self.local_path(*path))

class HTCondorWorkflow(law.contrib.htcondor.HTCondorWorkflow):
    """
    Batch systems are typically very heterogeneous by design, and so is HTCondor. Law does not aim
    to "magically" adapt to all possible HTCondor setups which would certainly end in a mess.
    Therefore we have to configure the base HTCondor workflow in law.contrib.htcondor to work with
    the VISPA environment. In most cases, like in this example, only a minimal amount of
    configuration is required.
    """

    htcondor_gpus = luigi.IntParameter(default=law.NO_INT, significant=False, description="number "
        "of GPUs to request on the VISPA cluster, leave empty to use only CPUs")

    def htcondor_output_directory(self):
        # the directory where submission meta data should be stored
        return law.LocalDirectoryTarget(self.local_path())

    def htcondor_create_job_file_factory(self):
        # tell the factory, which is responsible for creating our job files,
        # that the files are not temporary, i.e., it should not delete them after submission
        factory = super(HTCondorWorkflow, self).htcondor_create_job_file_factory()
        factory.is_tmp = False
        return factory

    def htcondor_bootstrap_file(self):
        # each job can define a bootstrap file that is executed prior to the actual job
        # in order to setup software and environment variables
        return law.util.rel_path(__file__, "bootstrap.sh")

    def htcondor_job_config(self, config, job_num, branches):
        # render_data is rendered into all files sent with a job
        config.render_variables["analysis_path"] = os.getenv("ANALYSIS_PATH")
        # copy the entire environment
        config.custom_content.append(("getenv", "true"))
        # tell the job config if GPUs are requested
        if not law.is_no_param(self.htcondor_gpus):
            config.custom_content.append(("request_gpus", self.htcondor_gpus))
        return config
