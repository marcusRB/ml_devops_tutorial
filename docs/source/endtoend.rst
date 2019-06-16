End to end MLOps
------------------------------
We will be using the Azure DevOps Project for build and release/deployment pipelines along with Azure ML services for model retraining pipeline, model management and operationalization.

.. image:: https://github.com/microsoft/MLOpsPython/raw/master/docs/images/ml-lifecycle.png

We now have 3 pipelines that we need to setup.

-  **Build Pipeline (azure-pipelines.yml)**: Runs tests and sets up
   infrastructure
-  **Retraining trigger pipeline(/template/retraining-template.json)**:
   This pipeline triggers Azure ML Pipeline (training/retraining) which
   trains a new model and publishes model image, if new model performs
   better
-  **Release pipeline(/template/release-template.json)**: This pipeline
   deploys and tests model image as web service in QA and Prod
   environment

.. note:: Start by cloning this repo https://github.com/trallard/MLOps_complementary
   And make sure to have followed the instructions on :ref:`GettingReady` 

1. Set up Build Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~

#. Select your devops organization and project by clicking dev.azure.com
#. Once you are in the right devops project, click Pipelines on the left
   hand menu and select Builds
#. Click **New pipeline** to create new pipeline

    .. image:: https://github.com/microsoft/MLOpsPython/raw/master/docs/images/new-build-pipeline1.png

#. | On the Connect option page, select **GitHub**
#. | On the Select option page, select the GitHub repository where you forked the code.
#. | Authorize Azure Pipelines to access your git account
#. | Since the repository contains azure-pipelines.yml at the root level, Azure DevOps recognizes it and auto imports it. Click **Run** and this will start the build pipeline.
#. | Your build run would look similar to the following image
   .. image:: https://github.com/microsoft/MLOpsPython/raw/master/docs/images/build-createpipeline1.png

Great, you now have the build pipeline setup, you can either manually
trigger it or it gets automatically triggered everytime there is a
change in the master branch.

**Note:** The build pipeline will perform basic test on the code and
provision infrastructure on azure. This can take around 10 mins to
complete.

2. Set up Retraining trigger release pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Note:** For setting up release pipelines, first download the
`release-pipelines <../release-pipelines>`__ to your local filesystem so
you can import it.

| To enable the option to **Import release pipeline**, we must have
atleast one release pipeline so let's create one with an empty job.

.. image:: https://github.com/microsoft/MLOpsPython/raw/master/docs/images/release-empty-job.png

| On the next screen, click on **Save** and then click **Ok** to save
the empty release pipeline.

.. image:: https://github.com/microsoft/MLOpsPython/raw/master/docs/images/release-save-empty.png


**Steps**

#. | Select the Release tab from the menu on the left, then click the
   New dropdown on top and click on **Import Release pipeline**

.. image:: https://github.com/microsoft/MLOpsPython/blob/master/docs/images/release-import.png


#. | On the next screen, navigate to **release-pipelines** folder and
   select **retrainingtrigger.json** pipeline file, click import. You
   should now see the following screen. Under Stages click on the
   Retrain stage, where it shows the red error sign.

.. image:: https://github.com/microsoft/MLOpsPython/raw/master/docs/images/release-retrainingtrigger.png


   | Click on agent job and then from the drop down for Agent Pool on
   the right side select **Hosted Ubuntu 1604** agent to execute your
   run and click **Save** button on top right.

.. image:: https://github.com/microsoft/MLOpsPython/raw/master/docs/images/release-retrainingagent.png

#. We would now link the variable group we created earlier to this
   release pipeline. To do so click on the **Variables** tab, then click
   on **Variable** groups and then select **Link variable group** and
   select the variable group that we created in previous step and click
   **Link** followed by **Save** button.

.. image:: https://github.com/microsoft/MLOpsPython/raw/master/docs/images/release-link-vg.png


#. | We want the retraining pipeline to be triggered every time build
   pipeline is complete. To create this dependency, we will link the
   artifact from build pipeline as a trigger for retraining trigger
   release pipeline. To do so, click on the **pipeline** tab and then
   select **Add an artifact** option under Artifacts.

.. image:: https://github.com/microsoft/MLOpsPython/raw/master/docs/images/release-retrainingpipeline.png

#. This will open up a pop up window, on this screen:

   -  for source type, select **Build**
   -  for project, select your project in Azure DevOps that you created
      in previous steps.
   -  For Source select the source build pipeline. If you have forked
      the git repo, the build pipeline may named
      ``yourgitusername.DevOpsForAI``
   -  In the Source alias, replace the auto-populated value with
      **``DevOpsForAI``**
   -  Field **Devault version** will get auto populated **Latest**, you
      can leave them as it is.
   -  Click on **Add**, and then **Save** the pipeline

.. image:: https://github.com/microsoft/MLOpsPython/raw/master/docs/images/release-retrainingartifact.png


#. Artifact is now added for retraining trigger pipeline, hit the
   **save** button on top right and then click **ok**.

#. | To trigger this pipeline every time build pipeline executes, click
   on the lighting sign to enable the **Continous Deployment Trigger**,
   click **Save**.

.. image:: https://github.com/microsoft/MLOpsPython/raw/master/docs/images/release-retrainingtrigger1.png


#. | If you want to run this pipeline on a schedule, you can set one by
   clicking on **Schedule set** in Artifacts section.

#. For the first time, we will manually trigger this pipeline.

-  Click Releases option on the left hand side and navigate to the
   release pipeline you just created.
-  Click **Create Release**
-  On the next screen click on **Create** button, this creates a manual
   release for you.

**Note**: This release pipeline will call the published AML pipeline.
The AML pipeline will train the model and package it into image. It will
take around 10 mins to complete. The next steps need this pipeline to
complete successfully.

3. Set up release (Deployment) pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Note:** For setting up release pipelines, first download the
`release-pipelines <../release-pipelines>`__ to your local filesystem so
you can import it.

**Also Note:** Before creating this pipeline, make sure that the build
pipeline, retraining trigger release pipeline and AML retraining
pipeline have been executed, as they will be creating resources during
their run like docker images that we will deploy as part of this
pipeline. So it is important for them to have successful runs before the
setup here.

Let's set up the release deployment pipeline now.

#. | As done in previous step, Select the Release tab from the menu on
   the left, then click the New dropdown on top and click on **Import
   Release pipeline**

#. | On the next screen, navigate to **release-pipelines** folder and
   select **releasedeployment.json** pipeline file, click import. You
   should now see the following screen. Under Stages click on the QA
   environment's \*\*view stage task", where it shows the red error
   sign.

.. image::  https://github.com/microsoft/MLOpsPython/raw/master/docs/images/release-deployment.png

   | Click on agent job and then from the drop down for Agent Pool on
   the right side select **Hosted Ubuntu 1604** agent to execute your
   run and click **Save** button on top right.

| Follow the same steps for **Prod Environment** and select **Hosted
Ubuntu 1604** for agent pool and save the pipeline.

#. | We would now link the variable group we created earlier to this
   release pipeline. To do so click on the **Variables** tab, then click
   on **Variable** groups and then select **Link variable group** and
   select the variable group that we created in previous step and click
   **Link** followed by **Save** button.

#. We now need to add artefact that will trigger this pipeline. We will
   add two artifacts:

   -  Build pipeline output as artifact since that contains our
      configuration and code files that we require in this pipeline.
   -  ACR artifact to trigger this pipeline everytime there is a new
      image that gets published to Azure container registry (ACR) as
      part of retraining pipeline.

Here are the steps to add build output as artifact

-  Click on pipeline tab to go back to pipeline view and click **Add an
   artifact**. This will open a pop up window

   -  for source type, select **Build**
   -  for project, select your project in Azure DevOps that you created
      in previous steps.
   -  For Source select the source build pipeline. If you have forked
      the git repo, the build pipeline may named
      ``yourgitusername.DevOpsForAI``
   -  In the Source alias, replace the auto-populated value with
      **``DevOpsForAI``**
   -  Field **Devault version** will get auto populated **Latest**, you
      can leave them as it is.
   -  Click on **Add**, and then **Save** the pipeline

.. image:: https://github.com/microsoft/MLOpsPython/raw/master/docs/images/release-retrainingartifact.png


Here are the steps to add ACR as an artifact
::

    - Click on pipeline tab to go back to pipeline view and click **Add an artifact**. This will open a pop up window
    - For Source type, click on **more artifact types** dropdown and select **Azure Container Registry**
    - For **service connection**, select an existing service connection to Azure, if you don't see anything in the dropdown, click on **Manage** and [create new **Azure Resource Manager**](https://docs.microsoft.com/en-us/azure/devops/pipelines/library/service-endpoints?view=azure-devops#create-a-service-connection) service connection for your subscription.
    **Note:** You must have sufficient privileges to create a service connection, if not contact your subscription adminstrator.
    - For Resource Group, select **DevOps_AzureML_Demo**, this is the default resource group name that we are using and if the previous pipelines executed properly you will see this resource group in the drop down.
    - Under Azure container registry dropdown, select the container registry, there should be only one container registry entry.
    - For repository, select **diabetes-model-score** repository.
    - For Default version, keep it to **latest**  
    - For Source alias, keep the default generated name.
    - Click Add
    - Click on lighting sign to enable the **Continous Deployment Trigger**, click Save.

    .. image:: https://github.com/microsoft/MLOpsPython/raw/master/docs/images/release-deploymentcitrigger.png
    

#. We now have QA environment continously deployed each time there is a
   new image available in container registry. You can select
   pre-deployment conditions for prod environment, normally you don't
   want it to be auto deployed, so select manual only trigger here.

.. image:: https://github.com/microsoft/MLOpsPython/raw/master/docs/images/release-deploymentprodtrigger.png


   To deploy a release manually, follow the document
   `here <https://docs.microsoft.com/en-us/azure/devops/pipelines/get-started-designer?view=azure-devops&tabs=new-nav#deploy-a-release>`__

Congratulations, you now have three pipelines set up end to end.

-  Build pipeline: triggered on code change to master branch on GitHub.
-  Release Trigger pipeline: triggered on build pipeline execution and
   produces a new model image if better than previous one.
-  Release Deployment pipeline: QA environment is auto triggered when
   there is a new image.
    Prod is manual only and user decides when to release to this
   environment.

.. |new build pipeline| image:: ./images/new-build-pipeline1.png
.. |build connnect step| image:: ./images/build-connect.png
.. |select repo| image:: ./images/build-selectrepo.png
.. |select repo| image:: ./images/Install_Azure_pipeline.png
.. |select repo| image:: ./images/build-createpipeline1.png
.. |select repo| image:: ./images/build-run.png
.. |import release pipeline| image:: ./images/release-new-pipeline.png
.. |import release pipeline| image:: ./images/release-empty-job.png
.. |import release pipeline| image:: ./images/release-save-empty.png
.. |import release pipeline| image:: ./images/release-import.png
.. |release retraining triggger| image:: ./images/release-retrainingtrigger.png
.. |release retraining agent| image:: ./images/release-retrainingagent.png
.. |release retraining artifact| image:: ./images/release-link-vg.png
.. |release pipeline view| image:: ./images/release-retrainingpipeline.png
.. |release retraining artifact| image:: ./images/release-retrainingartifact.png
.. |release retraining artifact| image:: ./images/release-retrainingtrigger1.png
.. |release retraining artifact| image:: ./images/release-retrainingartifactsuccess.png
.. |release retraining artifact| image:: ./images/release-createarelease.png
.. |release create| image:: ./images/release-create.png
.. |release retraining triggger| image:: ./images/release-deployment.png
.. |release retraining agent| image:: ./images/release-deploymentqaagent.png
.. |release retraining agent| image:: ./images/release-deploymentprodagent.png
.. |release retraining artifact| image:: ./images/release-link-vg.png
.. |release retraining artifact| image:: ./images/release-retrainingartifact.png
.. |release retraining agent| image:: ./images/release-deployment-service-conn.png
.. |release retraining artifact| image:: ./images/release-deploymentprodtrigger.png
