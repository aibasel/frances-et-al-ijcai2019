#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

from basilisk import BENCHMARK_DIR
from basilisk.incremental import IncrementalExperiment

from defaults import generate_experiment


def experiment(experiment_name=None):
    domain = "domain.pddl"
    domain_dir = "visitall"

    # Incremental version
    # Experiment used in the paper
    problem03full_incremental = dict(
        benchmark_dir=BENCHMARK_DIR,
        lp_max_weight=5,
        experiment_class=IncrementalExperiment,
        test_domain=domain,
        instances=['training01.pddl',
                   'training02.pddl',
                   'training03.pddl',
                   'training04.pddl',
                   'training05.pddl',
                   'training06.pddl',
                   'training09.pddl',
                   'training10.pddl',
                   'training11.pddl',],
        test_instances=["problem02-full.pddl",
                        "problem03-full.pddl",
                        "problem04-full.pddl",
                        "problem05-full.pddl",
                        "problem06-full.pddl",
                        "problem07-full.pddl",
                        "problem08-full.pddl",
                        "problem09-full.pddl",
                        "problem10-full.pddl",
                        "problem11-full.pddl",
                        'p-1-10.pddl',
                        'p-1-11.pddl',
                        'p-1-12.pddl',
                        'p-1-13.pddl',
                        'p-1-14.pddl',
                        'p-1-15.pddl',
                        'p-1-16.pddl',
                        'p-1-17.pddl',
                        'p-1-18.pddl',
                        'p-1-5.pddl',
                        'p-1-6.pddl',
                        'p-1-7.pddl',
                        'p-1-8.pddl',
                        'p-1-9.pddl',],
        num_states=10000,
        initial_sample_size=100,
        distance_feature_max_complexity=5,
        max_concept_grammar_iterations=10,
        initial_concept_bound=8, max_concept_bound=12, concept_bound_step=2,
        batch_refinement_size=50,
        clean_workspace=False,
        parameter_generator=add_domain_parameters,
        feature_namer=feature_namer,
    )

    parameters = {
        "problem03full_incremental": problem03full_incremental,
    }.get(experiment_name or "test")

    return generate_experiment(domain_dir, domain, **parameters)


def add_domain_parameters(language):
    return []


def feature_namer(feature):
    s = str(feature)
    return {
    }.get(s, s)


if __name__ == "__main__":
    exp = experiment(sys.argv[1])
    exp.run(sys.argv[2:])
