#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

from basilisk import BENCHMARK_DIR
from basilisk.incremental import IncrementalExperiment

from defaults import generate_experiment


def experiment(experiment_name=None):
    domain = "domain.pddl"
    domain_dir = "spanner"
    benchmark_dir = BENCHMARK_DIR

    # Experiment used in the paper
    spanner_1_incremental = dict(
        experiment_class=IncrementalExperiment,
        lp_max_weight=5,
        benchmark_dir=benchmark_dir,
        instances = ['training-1-1-5.pddl',
                     'training-2-1-5.pddl',
                     'training-2-2-5.pddl',
                     'training-3-1-5.pddl',
                     'training-3-3-5.pddl',
                     'training-4-2-5.pddl',
                     'training-4-4-5.pddl',
                     'training-5-3-5.pddl',
                     'training-5-4-5.pddl',
                     'training-5-5-5.pddl',
                     'training-1-1-6.pddl',
                     'training-1-1-20.pddl',],
        test_instances=["prob-3-3-3-1540903410.pddl",
                        "prob-4-3-3-1540907466.pddl",
                        "prob-4-3-3-1540907466.pddl",
                        "prob-10-10-10-1540903568.pddl",
                        "prob-15-10-8-1540913795.pddl",
                        "prob-10-10-25.pddl",
                        "prob-15-15-25.pddl"],
                        # "prob-20-15-40.pddl",
                        # "prob-20-20-50.pddl",],
        test_domain=domain,
        num_states=12000,
        initial_sample_size=100,
        max_concept_grammar_iterations=None,
        initial_concept_bound=8, max_concept_bound=12, concept_bound_step=2,
        batch_refinement_size=50,
        clean_workspace=False,
        parameter_generator=None,  # add_domain_parameters,
    )

    parameters = {
        "spanner_1_incremental": spanner_1_incremental,
    }.get(experiment_name or "test")

    return generate_experiment(domain_dir, domain, **parameters)


def generate_chosen_concepts(lang):
    """  """
    return [], [], []  # atoms, concepts, roles


def add_domain_parameters(language):
    return []


if __name__ == "__main__":
    exp = experiment(sys.argv[1])
    exp.run(sys.argv[2:])
